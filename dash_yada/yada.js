function escaping() {
    if (event.key == 'Escape' || event.which == 27 || event.code == 'Escape') {
        escaped = true
        paused = false
    }}

function nextItem() {paused = false}

const mouseClickEvents = ['mousedown', 'click', 'mouseup'];
function simulateMouseClick(element, args){
  mouseClickEvents.forEach(mouseEventType =>
    element.dispatchEvent(
      new MouseEvent(mouseEventType, {
          view: window,
          bubbles: true,
          cancelable: true,
          buttons: 1,
          target: element,
          ...args
      })
    )
  );
  mouseClickEvents.forEach(mouseEventType =>
    element.dispatchEvent(
      new PointerEvent(mouseEventType, {
          view: window,
          bubbles: true,
          cancelable: true,
          buttons: 1,
          target: element,
          ...args
      })
    )
  );
}

function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

async function play_script(data) {
    yada = document.querySelector(".yada")
    yada_img = document.querySelector(".yada > img")
    initialYada = yada.getBoundingClientRect()
    yada.style.top = initialYada.top + 'px'
    yada.style.left = initialYada.left + 'px'
    yada_img.classList.remove('sleeping')
    escaped = false
    document.addEventListener('keydown', escaping)
    yada.addEventListener('click', nextItem)
    for (y=0; y<data.length; y++) {
        target = document.querySelector(data[y].target)
        if (!target) {
            await delay(500)
        }
        target = document.querySelector(data[y].target)
        if (document.querySelector('.yada-convo')) {
            ReactDOM.render(
                React.createElement(
                    window.dash_core_components.Markdown, {style: {width:
                    document.querySelector('.yada-convo').getBoundingClientRect().width}}, data[y].convo
                ), document.querySelector('.yada-convo')
            )
        }

        if (target) {
            target.focus();
            try {
                target.select();
            } catch {
            }
            target.classList.toggle('highlighting')
            tBounds = target.getBoundingClientRect()
            yada.style.top = tBounds.top + tBounds.height/4+'px'
            yada.style.left = tBounds.left + tBounds.width/2.5 +'px'
            yada.setAttribute('convo', data[y].convo)
            setTimeout(() => {if (!isInViewport(target)) {
                window.scrollTo(tBounds.left, tBounds.top + yada.getBoundingClientRect().height + 15)
            }}, 1100)
            paused = true;
            previous = false;
            while (paused) {
                await delay(300)
            }

            if (escaped) {break}
            if (!previous) {
                if ('action' in data[y]) {
                    target.focus();
                    if (data[y]['action'] == 'click') {simulateMouseClick(target, data[y]['action_args'])}
                    if (data[y]['action'] == 'dblclick') {
                        simulateMouseClick(target, data[y]['action_args'])
                        setTimeout(() => simulateMouseClick(target, data[y]['action_args']), 100)
                        target.dispatchEvent(new Event('dblclick', {bubbles: true, view: window}))
                    }
                    if (data[y]['action'] == 'sendKeys') {
    //                  This will trigger a new render with the component
                        target.focus();
                        target.dispatchEvent(new KeyboardEvent('keydown', { bubbles: true, keepValue: true, view: window,
                         ...data[y]['action_args']}));
                        target.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true, keepValue: true, view: window,
                         ...data[y]['action_args']}));
                        await delay(100)
                    }
                    if (data[y]['action'] == 'type') {
                        // This will work by calling the native setter bypassing Reacts incorrect value change check
                        typing = document.querySelector(data[y].target);
                        Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')
                          .set.call(target, data[y]['action_args']);

    //                  This will trigger a new render with the component
                        typing.focus();
                        typing.dispatchEvent(new KeyboardEvent('change', { bubbles: true, keepValue: true}));
                        typing.dispatchEvent(new KeyboardEvent('input', { bubbles: true, keepValue: true}));
                        await delay(100)
                    }
                }
            }
            target.classList.toggle('highlighting')
        }
    }
    document.removeEventListener('keydown', escaping)
    document.querySelectorAll('.highlighting').forEach((t) => t.classList.remove('highlighting'))
    yada.removeEventListener('click', nextItem)

    // opens active_message
    yada.querySelector('div').dispatchEvent(new Event('click'))
    yada.removeAttribute('convo')
    yada.style.top = initialYada.top + 'px'
    yada.style.left = initialYada.left + 'px'
    yada.style.height = initialYada.height + 'px'
    await delay(1000)

    // closes active_message
    yada.querySelector('div').dispatchEvent(new Event('click'))
    yada_img.classList.add('sleeping')
    window.scrollTo(0,0)
    await delay(1000)
    yada.style.height = ''
    yada.style.top = ''
    yada.style.left = ''
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}