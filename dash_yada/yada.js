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
            setTimeout(
                () =>
                    simulateMouseClick(
                        document.querySelector('.yada_canvas_button_open')
                    ),
                100
            );
            if (data[dash_yada.y].target) {
                dash_yada.target = document.querySelector(
                    data[dash_yada.y].target
                );
                if (!dash_yada.target) {
                    await delay(500);
                }
                dash_yada.target = document.querySelector(
                    data[dash_yada.y].target
                );

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

                    dash_yada.yada.setAttribute(
                        'convo',
                        data[dash_yada.y].convo
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
                    if (!dash_yada.previous) {
                        if ('action' in data[dash_yada.y]) {
                            dash_yada.target.focus();
                            if (data[dash_yada.y].action === 'click') {
                                simulateMouseClick(
                                    dash_yada.target,
                                    data[dash_yada.y].action_args
                                );
                            }
                            if (data[dash_yada.y].action === 'dblclick') {
                                simulateMouseClick(
                                    dash_yada.target,
                                    data[dash_yada.y].action_args
                                );
                                setTimeout(
                                    () =>
                                        simulateMouseClick(
                                            dash_yada.target,
                                            data[dash_yada.y].action_args
                                        ),
                                    100
                                );
                                dash_yada.target.dispatchEvent(
                                    new Event('dblclick', {
                                        bubbles: true,
                                        view: window,
                                    })
                                );
                            }
                            if (data[dash_yada.y].action === 'sendKeys') {
                                //                  This will trigger a new render with the component
                                dash_yada.target.focus();
                                dash_yada.target.dispatchEvent(
                                    new KeyboardEvent('keydown', {
                                        bubbles: true,
                                        keepValue: true,
                                        view: window,
                                        ...data[dash_yada.y].action_args,
                                    })
                                );
                                dash_yada.target.dispatchEvent(
                                    new KeyboardEvent('keyup', {
                                        bubbles: true,
                                        keepValue: true,
                                        view: window,
                                        ...data[dash_yada.y].action_args,
                                    })
                                );
                                await delay(100);
                            }
                            if (data[dash_yada.y].action === 'type') {
                                // This will work by calling the native setter bypassing Reacts incorrect value change check
                                dash_yada.typing = document.querySelector(
                                    data[dash_yada.y].target
                                );
                                Object.getOwnPropertyDescriptor(
                                    window.HTMLInputElement.prototype,
                                    'value'
                                ).set.call(
                                    dash_yada.target,
                                    data[dash_yada.y].action_args
                                );

                                //                  This will trigger a new render with the component
                                dash_yada.typing.focus();
                                dash_yada.typing.dispatchEvent(
                                    new KeyboardEvent('change', {
                                        bubbles: true,
                                        keepValue: true,
                                    })
                                );
                                dash_yada.typing.dispatchEvent(
                                    new KeyboardEvent('input', {
                                        bubbles: true,
                                        keepValue: true,
                                    })
                                );
                                await delay(100);
                            }
                        }
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
