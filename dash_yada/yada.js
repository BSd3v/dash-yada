function escaping() {
    if (event.key == 'Escape' || event.which == 27 || event.code == 'Escape') {
        escaped = true
        paused = false
    }}

function nextItem() {paused = false}

const mouseClickEvents = ['mousedown', 'click', 'mouseup'];
function simulateMouseClick(element){
  mouseClickEvents.forEach(mouseEventType =>
    element.dispatchEvent(
      new MouseEvent(mouseEventType, {
          view: window,
          bubbles: true,
          cancelable: true,
          buttons: 1,
          target: element,
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
      })
    )
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
            paused = true
            while (paused) {
                await delay(300)
            }
            if (escaped) {break}
            if ('action' in data[y]) {
                target.focus();
                if (data[y]['action'] == 'click') {simulateMouseClick(target)}
                if (data[y]['action'] == 'dblclick') {
                    simulateMouseClick(target)
                    setTimeout(() => simulateMouseClick(target), 100)
                }
                if (data[y]['action'] == 'send_keys') {
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
    await delay(1000)
    yada.style.height = ''
    yada.style.top = ''
    yada.style.left = ''
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}