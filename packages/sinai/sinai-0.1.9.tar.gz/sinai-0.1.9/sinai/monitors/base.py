"""
The Monitor connects to sources, evaluates rules, sends the resulting metrics to the stores.
"""
from __future__ import annotations

import sys
from collections.abc import Iterable
from typing import get_type_hints
from uuid import uuid4

from sinai.exceptions import SourceError, SourceNotFound
from sinai.metrics import Metric
from sinai.rules import Rule
from sinai.sources import MetricSource
from sinai.types import (
    Evaluation,
    JDict,
    OptionalSourceInstances,
    RuleClass,
    RuleClasses,
    SourceClass,
    SourceClassList,
    SourceDict,
    SourceInstance,
    StoreClass,
    StoreClassList,
    StoreDict,
)


class Monitor:
    """The monitor controls the monitoring run."""

    rules: RuleClasses = []
    context: str = "global"

    def __init__(self) -> None:
        self.id = str(uuid4())
        self.sources: SourceClassList = []
        self.stores: StoreClassList = []
        self._store_instances: StoreDict = {}
        self._source_instances: SourceDict = {}
        self._source_map = {}  # type: ignore
        self._resolve_rules()

    def _add_source(self, source_cls: SourceClass) -> None:
        if source_cls not in self.sources:
            self.sources.append(source_cls)

    def _add_store(self, store_cls: StoreClass) -> None:
        if store_cls not in self.stores:
            self.stores.append(store_cls)

    def __resolve_stores_from_attribute(self, rule_cls: RuleClass) -> None:
        """Get the stores from stores = []"""
        for store_cls in rule_cls.stores:
            self._add_store(store_cls)

    def __resolve_sources_from_attribute(self, rule_cls: RuleClass) -> None:
        """Get the sources from sources = []"""
        for source_cls in rule_cls.sources:
            self._add_source(source_cls)

    def _get_annotations(self, rule_cls: RuleClass) -> JDict:
        """Getting annonations for the constructor."""
        if sys.version_info.minor > 8:
            try:
                return get_type_hints(rule_cls.__init__, include_extras=True)
            except NameError:
                pass

        try:
            return get_type_hints(rule_cls.__init__)
        except NameError:
            pass

        return rule_cls.__init__.__annotations__

    def __resolve_sources_from_init(self, rule_cls: RuleClass) -> None:
        self._source_map[rule_cls] = {}
        annos = self._get_annotations(rule_cls)
        for arg, source_cls in annos.items():
            if arg == "monitor":
                self._source_map[rule_cls]["monitor"] = self.__class__
            elif arg == "return":
                continue
            elif source_cls == "MetricSource":
                self._add_source(MetricSource)
                self._source_map[rule_cls][arg] = MetricSource
            else:
                self._add_source(source_cls)
                self._source_map[rule_cls][arg] = source_cls

    def _resolve_rules(self) -> None:
        for rule_cls in self.rules:
            self.__resolve_stores_from_attribute(rule_cls)
            self.__resolve_sources_from_attribute(rule_cls)
            self.__resolve_sources_from_init(rule_cls)

    def _connect_sources(self) -> None:
        for source_class in self.sources:
            try:
                self._source_instances[source_class] = source_class(monitor=self)
            except TypeError:
                raise SourceError(
                    f"The object {source_class} is not a valid Source class."
                )

    def _connect_stores(self) -> None:
        for store_class in self.stores:
            self._store_instances[store_class] = store_class(monitor=self)

    def _evaluate_rules(self) -> None:
        for rule_class in self.rules:
            self._evaluate_rule(rule_class)

    def _get_rule_sources(self, rule_cls: RuleClass) -> OptionalSourceInstances:
        return [self.source(source) for source in rule_cls.sources]

    def _get_rule_args(self, rule_cls: RuleClass):
        kwargs: JDict = {}
        for arg, source_cls in self._source_map[rule_cls].items():
            if arg == "monitor":
                kwargs["monitor"] = self
            else:
                kwargs[arg] = self.source(source_cls)

        return kwargs

    def _evaluate_rule(self, rule_class: RuleClass) -> None:
        kwargs = self._get_rule_args(rule_class)
        rule = rule_class(**kwargs)
        if "monitor" not in kwargs:
            rule.monitor = self
        result: Evaluation = rule.evaluate()
        if isinstance(result, Iterable):
            for metric in result:
                self.store_metric(rule, metric)
        elif not result:
            return
        else:
            self.store_metric(rule, result)

    def execute(self) -> None:
        """Start monitoring."""
        self._connect_stores()
        self._connect_sources()
        self._evaluate_rules()

    def source(self, source: SourceClass) -> SourceInstance:
        """Return an instatatied source."""
        try:
            return self._source_instances[source]
        except KeyError:
            raise SourceNotFound(f"Could not find {source.__name__} source instance.")

    def store_metric(self, rule: Rule, metric: Metric) -> None:
        """Store a metric."""
        if not metric.context:
            metric.context = self.context
        for store_class in rule.stores:
            store = self._store_instances[store_class]
            store.save_metric(metric)
