from contextlib import contextmanager
from typing import (
    Any,
    ContextManager,
    Generator,
    List,
    Mapping,
    Optional,
    Sequence,
    TypeVar,
)

from di._utils.types import FusedContextManager
from di.api.dependencies import DependentBase
from di.api.executor import SupportsAsyncExecutor, SupportsSyncExecutor
from di.api.providers import DependencyProvider
from di.api.scopes import Scope
from di.api.solved import SolvedDependent
from di.container._bind_hook import BindHook
from di.container._execution_planning import plan_execution
from di.container._solving import ScopeResolver, solve
from di.container._state import ContainerState

DependencyType = TypeVar("DependencyType")


class Container:
    """Solve and execute dependencies.

    Generally you will want one Container per application.
    There is not performance advantage to re-using a container, the only reason to do so is to share binds.
    For each "thing" you want to wire with di and execute you'll want to call `Container.solve()`
    exactly once and then keep a reference to the returned `SolvedDependent` to pass to `Container.execute`.
    Solving is very expensive so avoid doing it in a hot loop.
    """

    __slots__ = ("_bind_hooks", "_state")

    _bind_hooks: List[BindHook]

    def __init__(self) -> None:
        self._bind_hooks = []

    def bind(
        self,
        hook: BindHook,
    ) -> ContextManager[None]:
        """Replace a dependency provider with a new one.

        This can be used as a function (for a permanent bind, cleared when `scope` is exited)
        or as a context manager (the bind will be cleared when the context manager exits).
        """

        self._bind_hooks.append(hook)

        @contextmanager
        def unbind() -> "Generator[None, None, None]":
            try:
                yield
            finally:
                self._bind_hooks.remove(hook)

        return unbind()

    def solve(
        self,
        dependency: DependentBase[DependencyType],
        scopes: Sequence[Scope],
        scope_resolver: Optional[ScopeResolver] = None,
    ) -> SolvedDependent[DependencyType]:
        """Build the dependency graph.

        Should happen once, maybe during startup.

        Solving dependencies can be slow.
        """
        return solve(dependency, scopes, self._bind_hooks, scope_resolver)

    def execute_sync(
        self,
        solved: SolvedDependent[DependencyType],
        executor: SupportsSyncExecutor,
        *,
        state: ContainerState,
        values: Optional[Mapping[DependencyProvider, Any]] = None,
    ) -> DependencyType:
        """Execute an already solved dependency.

        This method is synchronous and uses a synchronous executor,
        but the executor may still be able to execute async dependencies.
        """
        results, ts, execution_state, root_task = plan_execution(
            stacks=state.stacks,
            cache=state.cached_values,
            solved=solved,
            values=values,
        )
        executor.execute_sync(ts, execution_state)
        return results[root_task.task_id]  # type: ignore[no-any-return]

    async def execute_async(
        self,
        solved: SolvedDependent[DependencyType],
        executor: SupportsAsyncExecutor,
        *,
        state: ContainerState,
        values: Optional[Mapping[DependencyProvider, Any]] = None,
    ) -> DependencyType:
        """Execute an already solved dependency."""
        results, ts, execution_state, root_task = plan_execution(
            stacks=state.stacks,
            cache=state.cached_values,
            solved=solved,
            values=values,
        )
        await executor.execute_async(ts, execution_state)
        return results[root_task.task_id]  # type: ignore[no-any-return]

    def enter_scope(
        self, scope: Scope, state: Optional[ContainerState] = None
    ) -> FusedContextManager[ContainerState]:
        state = state or ContainerState()
        return state.enter_scope(scope)
