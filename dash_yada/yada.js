var dash_yada = (window.dash_yada = window.dash_yada || {});
function escaping() {
    if (
        event.key === 'Escape' ||
        event.which === 27 || // eslint-disable-line no-magic-numbers
        event.code === 'Escape'
    ) {
        dash_yada.escaped = true;
        dash_yada.paused = false;
    }
}

function nextItem() {
    dash_yada.paused = false;
}

const mouseClickEvents = ['mousedown', 'click', 'mouseup'];
const touchClickEvents = ['touchstart', 'touchend', 'click'];
function simulateMouseClick(element, args) {
    if (!/Android|iPhone/i.test(navigator.userAgent)) {
        mouseClickEvents.forEach((mouseEventType) =>
            element.dispatchEvent(
                new MouseEvent(mouseEventType, {
                    view: window,
                    bubbles: true,
                    cancelable: true,
                    buttons: 1,
                    target: element,
                    ...args,
                })
            )
        );
    } else {
        touchClickEvents.forEach((mouseEventType) =>
            element.dispatchEvent(
                new TouchEvent(mouseEventType, {
                    view: window,
                    bubbles: true,
                    cancelable: true,
                    buttons: 1,
                    target: element,
                    ...args,
                })
            )
        );
    }
}

function isInViewport(element) {
    if (!element) {
        return true;
    }
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <=
            (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <=
            (window.innerWidth || document.documentElement.clientWidth)
    );
}

function isInViewportFunc(rect) {
    if (!rect) {
        return true;
    }
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <=
            (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <=
            (window.innerWidth || document.documentElement.clientWidth)
    );
}

function hasVisibleConvo(step) {
    return (
        step &&
        typeof step.convo === 'string' &&
        step.convo.trim() !== '' &&
        step.show_text !== false
    );
}

function deepClone(value) {
    if (value === undefined) {
        return undefined;
    }
    try {
        return JSON.parse(JSON.stringify(value));
    } catch {
        return value;
    }
}

function normalizePath(path) {
    if (Array.isArray(path)) {
        return path;
    }
    if (typeof path === 'number') {
        return [path];
    }
    if (typeof path === 'string') {
        const trimmed = path.trim();
        if (trimmed === '') {
            return [];
        }

        // Prefer Dash-style list paths, including stringified JSON lists.
        if (trimmed.startsWith('[') && trimmed.endsWith(']')) {
            try {
                const parsed = JSON.parse(trimmed);
                if (Array.isArray(parsed)) {
                    return parsed;
                }
            } catch {
                // Fall back to dot-path parsing below.
            }
        }

        return trimmed
            .split('.')
            .filter((p) => p !== '')
            .map((p) => {
                const n = Number(p);
                return Number.isInteger(n) && String(n) === p ? n : p;
            });
    }
    return [];
}

function getByPath(root, path) {
    return normalizePath(path).reduce((acc, key) => {
        if (acc === null || acc === undefined) {
            return undefined;
        }
        return acc[key];
    }, root);
}

function getPathParent(root, path) {
    const parts = normalizePath(path);
    if (parts.length === 0) {
        return [null, null];
    }
    const parent = parts.slice(0, -1).reduce((acc, key) => {
        if (acc === null || acc === undefined) {
            return undefined;
        }
        return acc[key];
    }, root);
    return [parent, parts[parts.length - 1]];
}

function getCurrentComponentProps(componentId) {
    if (
        window.dash_component_api &&
        typeof window.dash_component_api.getComponentLayout === 'function'
    ) {
        const layout = window.dash_component_api.getComponentLayout(componentId);
        if (layout && layout.props && typeof layout.props === 'object') {
            return layout.props;
        }
    }
    return {};
}

function buildPatchPayload(componentId, actionArgs) {
    actionArgs = actionArgs || {};
    const patchSpec = actionArgs.patch || actionArgs.patches;
    if (!patchSpec) {
        return {};
    }

    if (!window.dash_clientside || typeof window.dash_clientside.Patch !== 'function') {
        return {};
    }

    const currentProps = getCurrentComponentProps(componentId);
    const payload = {};

    const applyToProp = (propName, spec) => {
        if (!propName) {
            return;
        }
        const patch = new window.dash_clientside.Patch();
        let working = deepClone(currentProps[propName]);

        const applyOps = (ops) => {
            (ops || []).forEach((operation) => {
                const op = operation.op || operation.type || 'set';
                const path = normalizePath(operation.path || operation.key || []);
                const opValue = deepClone(operation.value);

                if (op === 'replace') {
                    if (path.length === 0) {
                        payload[propName] = opValue;
                        working = deepClone(opValue);
                        return;
                    }
                    patch.assign(path, opValue);
                    if (working === null || typeof working !== 'object') {
                        working = {};
                    }
                    const [parent, leaf] = getPathParent(working, path);
                    if (parent && typeof parent === 'object') {
                        parent[leaf] = deepClone(opValue);
                    }
                    return;
                }

                if (op === 'set') {
                    if (path.length === 0) {
                        payload[propName] = opValue;
                        working = deepClone(opValue);
                        return;
                    }
                    patch.assign(path, opValue);
                    if (working === null || typeof working !== 'object') {
                        working = {};
                    }
                    const [parent, leaf] = getPathParent(working, path);
                    if (parent && typeof parent === 'object') {
                        parent[leaf] = deepClone(opValue);
                    }
                    return;
                }

                if (op === 'merge') {
                    const mergeValue =
                        opValue && typeof opValue === 'object' ? opValue : {};
                    const current =
                        path.length > 0 ? getByPath(working, path) : working;
                    const merged = {
                        ...(current && typeof current === 'object' ? current : {}),
                        ...mergeValue,
                    };
                    patch.assign(path, merged);
                    if (path.length === 0) {
                        working = deepClone(merged);
                    } else if (working && typeof working === 'object') {
                        const [parent, leaf] = getPathParent(working, path);
                        if (parent && typeof parent === 'object') {
                            parent[leaf] = deepClone(merged);
                        }
                    }
                    return;
                }

                if (op === 'append') {
                    const current = path.length > 0 ? getByPath(working, path) : working;
                    const next = Array.isArray(current) ? [...current, opValue] : [opValue];
                    patch.assign(path, next);
                    if (path.length === 0) {
                        working = deepClone(next);
                    }
                    return;
                }

                if (op === 'prepend') {
                    const current = path.length > 0 ? getByPath(working, path) : working;
                    const next = Array.isArray(current) ? [opValue, ...current] : [opValue];
                    patch.assign(path, next);
                    if (path.length === 0) {
                        working = deepClone(next);
                    }
                    return;
                }

                if (op === 'extend') {
                    const values = Array.isArray(opValue) ? opValue : [opValue];
                    const current = path.length > 0 ? getByPath(working, path) : working;
                    const next = Array.isArray(current) ? [...current, ...values] : [...values];
                    patch.assign(path, next);
                    if (path.length === 0) {
                        working = deepClone(next);
                    }
                    return;
                }

                if (op === 'insert') {
                    const index = Number.isInteger(operation.index)
                        ? operation.index
                        : 0;
                    const current = path.length > 0 ? getByPath(working, path) : working;
                    const next = Array.isArray(current) ? [...current] : [];
                    next.splice(index, 0, opValue);
                    patch.assign(path, next);
                    if (path.length === 0) {
                        working = deepClone(next);
                    }
                    return;
                }

                if (op === 'clear') {
                    const current = path.length > 0 ? getByPath(working, path) : working;
                    const next = Array.isArray(current)
                        ? []
                        : current && typeof current === 'object'
                          ? {}
                          : null;
                    patch.assign(path, next);
                    if (path.length === 0) {
                        working = deepClone(next);
                    }
                    return;
                }

                if (op === 'reverse') {
                    const current = path.length > 0 ? getByPath(working, path) : working;
                    const next = Array.isArray(current) ? [...current].reverse() : current;
                    patch.assign(path, next);
                    if (path.length === 0 && Array.isArray(next)) {
                        working = deepClone(next);
                    }
                    return;
                }

                if (op === 'remove' || op === 'delete') {
                    if (path.length === 0) {
                        return;
                    }
                    const parentPath = path.slice(0, -1);
                    const leaf = path[path.length - 1];
                    const parentCurrent =
                        parentPath.length > 0 ? getByPath(working, parentPath) : working;
                    if (Array.isArray(parentCurrent) && typeof leaf === 'number') {
                        const next = [...parentCurrent];
                        next.splice(leaf, 1);
                        patch.assign(parentPath, next);
                    } else if (parentCurrent && typeof parentCurrent === 'object') {
                        const next = { ...parentCurrent };
                        delete next[leaf];
                        patch.assign(parentPath, next);
                    }
                }
            });
        };

        if (Array.isArray(spec)) {
            applyOps(spec);
            if (!(propName in payload)) {
                payload[propName] = patch.build();
            }
            return;
        }
        if (spec && typeof spec === 'object') {
            if (Array.isArray(spec.ops || spec.operations)) {
                applyOps(spec.ops || spec.operations);
                if (!(propName in payload)) {
                    payload[propName] = patch.build();
                }
                return;
            }
            if ('value' in spec) {
                payload[propName] = deepClone(spec.value);
                return;
            }
            payload[propName] = patch.build();
        }
    };

    if (Array.isArray(patchSpec)) {
        const propName = actionArgs.prop || actionArgs.property;
        applyToProp(propName, patchSpec);
        return payload;
    }

    if (patchSpec && typeof patchSpec === 'object') {
        if (patchSpec.props && typeof patchSpec.props === 'object') {
            Object.entries(patchSpec.props).forEach(([propName, spec]) => {
                applyToProp(propName, spec);
            });
        }
        if (patchSpec.prop || patchSpec.property) {
            applyToProp(
                patchSpec.prop || patchSpec.property,
                patchSpec.ops || patchSpec.operations || patchSpec
            );
        }
    }

    return payload;
}

async function runScriptAction(step, target) {
    if (!step || !('action' in step)) {
        return;
    }

    if (step.action === 'click') {
        simulateMouseClick(target, step.action_args);
    }
    if (step.action === 'dblclick') {
        simulateMouseClick(target, step.action_args);
        setTimeout(() => {
            simulateMouseClick(target, step.action_args);
            target.dispatchEvent(
                new MouseEvent('dblclick', {
                    bubbles: true,
                    cancelable: true,
                    composed: true,
                    detail: 2,
                    button: 0,
                    buttons: 1,
                    view: window,
                    ...step.action_args,
                })
            );
        }, 100);
    }
    if (step.action === 'sendKeys') {
        const actionArgs = step.action_args || {};
        const keyValue =
            typeof actionArgs.key === 'string'
                ? actionArgs.key
                : typeof actionArgs.text === 'string'
                  ? actionArgs.text
                  : typeof actionArgs.value === 'string'
                    ? actionArgs.value
                    : '';
        const isEditableTarget =
            target &&
            (target instanceof HTMLInputElement ||
                target instanceof HTMLTextAreaElement ||
                target.isContentEditable);

        target.focus();
        const keydownEvent = new KeyboardEvent('keydown', {
            bubbles: true,
            cancelable: true,
            view: window,
            ...actionArgs,
        });
        const shouldApplyDefault = target.dispatchEvent(keydownEvent);

        if (shouldApplyDefault && isEditableTarget && keyValue) {
            if (
                target instanceof HTMLInputElement ||
                target instanceof HTMLTextAreaElement
            ) {
                const prototype =
                    target instanceof HTMLInputElement
                        ? window.HTMLInputElement.prototype
                        : window.HTMLTextAreaElement.prototype;
                Object.getOwnPropertyDescriptor(prototype, 'value').set.call(
                    target,
                    target.value + keyValue
                );
            } else if (target.isContentEditable) {
                target.textContent = `${target.textContent || ''}${keyValue}`;
            }

            target.dispatchEvent(
                new InputEvent('input', {
                    bubbles: true,
                    data: keyValue,
                    inputType: 'insertText',
                })
            );
            target.dispatchEvent(new Event('change', { bubbles: true }));
        }

        target.dispatchEvent(
            new KeyboardEvent('keypress', {
                bubbles: true,
                cancelable: true,
                view: window,
                ...actionArgs,
            })
        );
        target.dispatchEvent(
            new KeyboardEvent('keyup', {
                bubbles: true,
                cancelable: true,
                view: window,
                ...actionArgs,
            })
        );
        await delay(100);
    }
    if (step.action === 'type') {
        const typingElement = document.querySelector(step.target);
        Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype,
            'value'
        ).set.call(target, step.action_args);
        typingElement.focus();
        typingElement.dispatchEvent(
            new KeyboardEvent('change', {
                bubbles: true,
                keepValue: true,
            })
        );
        typingElement.dispatchEvent(
            new KeyboardEvent('input', {
                bubbles: true,
                keepValue: true,
            })
        );
        await delay(100);
    }
    if (step.action === 'set_props') {
        const actionArgs = step.action_args || {};
        let setPropsId = actionArgs.id || step.set_props_id || step.target;
        if (typeof setPropsId === 'string' && setPropsId.startsWith('#')) {
            setPropsId = setPropsId.slice(1);
        }
        const setPropsPayload =
            actionArgs.props && typeof actionArgs.props === 'object'
                ? actionArgs.props
                : Object.fromEntries(
                      Object.entries(actionArgs).filter(
                          ([key]) =>
                              key !== 'id' &&
                              key !== 'patch' &&
                              key !== 'patches' &&
                              key !== 'prop' &&
                              key !== 'property'
                      )
                  );
        const patchPayload = buildPatchPayload(setPropsId, actionArgs);
        const finalPayload = { ...setPropsPayload, ...patchPayload };

        if (
            setPropsId &&
            Object.keys(finalPayload).length > 0 &&
            window.dash_clientside &&
            window.dash_clientside.set_props
        ) {
            window.dash_clientside.set_props(setPropsId, finalPayload);
            await delay(100);
        }
    }
}

/* eslint-disable no-magic-numbers, no-unused-vars*/
async function play_script(data) {
    /* eslint-enable no-unused-vars*/
    dash_yada.script_length = data.length;
    dash_yada.yada = document.querySelector('.yada');
    dash_yada.yada_img = document.querySelector('.yada > img');
    dash_yada.initialYada = dash_yada.yada.getBoundingClientRect();
    dash_yada.yada.style.top = dash_yada.initialYada.top + 'px';
    dash_yada.yada.style.left = dash_yada.initialYada.left + 'px';
    dash_yada.yada_img.classList.remove('sleeping');
    dash_yada.yada.classList.remove('sleeping');
    dash_yada.escaped = false;
    document.addEventListener('keydown', escaping);
    dash_yada.yada.addEventListener('click', nextItem);
    dash_yada.placement = 'bottom';
    dash_yada.yada.classList.remove('activated');
    dash_yada.yada.classList.add('script-running');
    dash_yada.yada.classList.remove('script-ended');

    dash_yada.reopen = false;
    for (dash_yada.y = 0; dash_yada.y < data.length; dash_yada.y++) {
        if (dash_yada.y === 0) {
            if (document.querySelector('.yada-info')) {
                document.querySelector('.yada-info .previous').style.display =
                    '';
            }
        }
        if (dash_yada.y >= dash_yada.script_length - 1) {
            if (document.querySelector('.yada-info')) {
                document.querySelector('.yada-info .next').style.display =
                    'none';
            }
        }
        if (dash_yada.y < dash_yada.script_length - 1) {
            if (document.querySelector('.yada-info')) {
                document.querySelector('.yada-info .next').style.display =
                    'initial';
            }
        }
        if (data[dash_yada.y]) {
            const currentStep = data[dash_yada.y];
            if (hasVisibleConvo(currentStep)) {
                setTimeout(
                    () =>
                        simulateMouseClick(
                            document.querySelector('.yada_canvas_button_open')
                        ),
                    100
                );
            }
            if (currentStep.target) {
                dash_yada.target = document.querySelector(currentStep.target);
                if (!dash_yada.target) {
                    await delay(500);
                }
                dash_yada.target = document.querySelector(currentStep.target);

                if (dash_yada.target) {
                    try {
                        dash_yada.target.select();
                        dash_yada.target.focus();
                    } catch {
                        dash_yada.target.focus();
                    }
                    dash_yada.target.classList.add('highlighting');
                    dash_yada.tBounds =
                        dash_yada.target.getBoundingClientRect();
                    if (!isInViewport(dash_yada.target)) {
                        //                window.scrollTo(dash_yada.tBounds.left, dash_yada.tBounds.top);
                        await delay(100);
                        dash_yada.tBounds =
                            dash_yada.target.getBoundingClientRect();
                        setTimeout(() => {
                            window.scrollTo(
                                dash_yada.tBounds.left - 20,
                                dash_yada.tBounds.top - 20
                            );
                        }, 1000);
                    }

                    var newLocation = {
                        top:
                            dash_yada.tBounds.top +
                            dash_yada.tBounds.height / 4 +
                            window.scrollY,
                        left:
                            dash_yada.tBounds.left +
                            dash_yada.tBounds.width / 2.5 +
                            window.scrollX,
                        bottom:
                            dash_yada.tBounds.top +
                            dash_yada.tBounds.height / 4 +
                            window.scrollY +
                            dash_yada.yada.getBoundingClientRect().height,
                        right:
                            dash_yada.tBounds.left +
                            dash_yada.tBounds.width / 2.5 +
                            window.scrollX +
                            dash_yada.yada.getBoundingClientRect().width,
                    };

                    if (!isInViewportFunc(newLocation)) {
                        var newTop = newLocation.top;
                        var newLeft = newLocation.left;

                        if (
                            newLocation.top > dash_yada.tBounds.top &&
                            newLocation.top + dash_yada.tBounds.height >
                                window.innerHeight
                        ) {
                            newTop =
                                dash_yada.tBounds.top +
                                window.scrollY -
                                dash_yada.yada.getBoundingClientRect().height +
                                (dash_yada.tBounds.top +
                                    window.scrollY -
                                    newLocation.top);
                        }
                        if (
                            newLocation.left > dash_yada.tBounds.left &&
                            newLocation.left +
                                dash_yada.yada.getBoundingClientRect().width >
                                window.innerWidth
                        ) {
                            newLeft =
                                dash_yada.tBounds.left +
                                window.scrollX -
                                dash_yada.yada.getBoundingClientRect().width +
                                (dash_yada.tBounds.left +
                                    window.scrollX -
                                    newLocation.left);
                        }
                        newLocation.top = newTop;
                        newLocation.left = newLeft;
                    }
                    dash_yada.yada.style.top = newLocation.top + 'px';
                    dash_yada.yada.style.left = newLocation.left + 'px';

                    if (hasVisibleConvo(currentStep)) {
                        dash_yada.yada.setAttribute(
                            'convo',
                            currentStep.convo
                        );
                        if (dash_yada.y > 0 || dash_yada.reopen) {
                            dash_yada.offcanvas =
                                document.querySelector('.yada-info');
                            if (!dash_yada.offcanvas) {
                                simulateMouseClick(
                                    document.querySelector(
                                        '.yada_canvas_button_open'
                                    )
                                );
                                while (!dash_yada.offcanvas) {
                                    await delay(300);
                                    dash_yada.offcanvas =
                                        document.querySelector('.yada-info');
                                }
                            }
                        }
                        try {
                            if (dash_yada.y !== dash_yada.last) {
                                setTimeout(() => {
                                    if (
                                        ((document
                                            .querySelector('.yada-info')
                                            .getBoundingClientRect().top >
                                            dash_yada.yada.getBoundingClientRect()
                                                .top &&
                                            document
                                                .querySelector('.yada-info')
                                                .getBoundingClientRect().top <
                                                dash_yada.yada.getBoundingClientRect()
                                                    .top +
                                                    dash_yada.yada.getBoundingClientRect()
                                                        .height /
                                                        2) ||
                                            document
                                                .querySelector('.yada-info')
                                                .getBoundingClientRect().top <
                                                dash_yada.yada.getBoundingClientRect()
                                                    .top) &&
                                        dash_yada.placement === 'bottom'
                                    ) {
                                        dash_yada.placement = 'top';
                                    } else if (
                                        document
                                            .querySelector('.yada-info')
                                            .getBoundingClientRect().height >
                                            dash_yada.yada.getBoundingClientRect()
                                                .top &&
                                        dash_yada.placement === 'top'
                                    ) {
                                        dash_yada.placement = 'bottom';
                                    }
                                    setTimeout(() => {
                                        simulateMouseClick(
                                            document.querySelector(
                                                '.yada_canvas_button_open'
                                            )
                                        );
                                    }, 100);
                                    dash_yada.last = dash_yada.y;
                                }, 1500);
                            }
                        } catch (err) {
                            console.log(err);
                        }

                        dash_yada.paused = true;
                        dash_yada.previous = false;
                        if (document.querySelector('.yada-info')) {
                            if (dash_yada.y !== 0) {
                                document.querySelector(
                                    '.yada-info .previous'
                                ).style.display = 'initial';
                            }
                            if (dash_yada.y < dash_yada.script_length - 1) {
                                document.querySelector(
                                    '.yada-info .next'
                                ).style.display = 'initial';
                            }
                        }

                        dash_yada.reopen = true;
                        while (dash_yada.paused) {
                            await delay(300);
                        }

                        if (dash_yada.escaped) {
                            break;
                        }
                        if (!document.querySelector('.yada-info')) {
                            dash_yada.previous = true;
                            dash_yada.y--;
                        }
                    } else {
                        dash_yada.yada.removeAttribute('convo');
                        dash_yada.paused = false;
                        dash_yada.previous = false;
                    }
                    if (!dash_yada.previous) {
                        dash_yada.target.focus();
                        await runScriptAction(currentStep, dash_yada.target);
                    } else {
                        while (
                            !document.querySelector(
                                data[dash_yada.y + 1].target
                            ) &&
                            dash_yada.y !== -1
                        ) {
                            dash_yada.y--;
                        }
                    }

                    dash_yada.target.classList.remove('highlighting');
                }
            } else if (currentStep.action === 'set_props') {
                await runScriptAction(currentStep, null);
            }
        }
    }

    dash_yada.yada.classList.add('script-ended');

    if (document.querySelector('.yada-info')) {
        document.querySelector('.yada-info .next').style.display = 'none';
        document.querySelector('.yada-info .previous').style.display = '';
    }

    document.removeEventListener('keydown', escaping);
    document
        .querySelectorAll('.highlighting')
        .forEach((t) => t.classList.remove('highlighting'));
    dash_yada.yada.removeEventListener('click', nextItem);

    document.querySelector('.sleepy_yada').dispatchEvent(new Event('click'));
    dash_yada.yada.style.top = dash_yada.initialYada.top + 'px';
    dash_yada.yada.style.left = dash_yada.initialYada.left + 'px';
    dash_yada.yada.style.height = dash_yada.initialYada.height + 'px';
    dash_yada.yada.style.width = dash_yada.initialYada.width + 'px';
    await delay(1000);

    document.querySelector('.sleepy_yada').dispatchEvent(new Event('click'));
    dash_yada.yada_img.classList.add('sleeping');
    dash_yada.yada.classList.add('sleeping');
    dash_yada.yada.removeAttribute('convo');
    window.scrollTo(0, 0);
    await delay(1000);
    dash_yada.yada.style.height = '';
    dash_yada.yada.style.top = '';
    dash_yada.yada.style.left = '';
    dash_yada.yada.style.width = '';

    // resetting placement
    dash_yada.placement = 'bottom';
    setTimeout(() => {
        simulateMouseClick(document.querySelector('.yada_canvas_button_open'));
        dash_yada.yada.classList.remove('script-running');
    }, 1000);
}
/* eslint-enable no-magic-numbers */

function delay(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}
