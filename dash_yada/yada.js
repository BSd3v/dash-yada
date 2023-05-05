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
          buttons: 1
      })
    )
  );
}

async function playScript(data) {
    yada = document.querySelector(".yada")
    yada_img = document.querySelector(".yada > img")
    yada.style.top = '0px'
    yada.style.left = document.body.getBoundingClientRect().width - 30
     - yada.getBoundingClientRect().width + 'px'
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
                if (data[y]['action'] == 'click') {simulateMouseClick(target)}
                if (data[y]['action'] == 'dblclick') {
                    simulateMouseClick(target)
                    setTimeout(() => simulateMouseClick(target), 100)
                }
                if (data[y]['action'] == 'send_keys') {
                    // This will work by calling the native setter bypassing Reacts incorrect value change check
                    Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')
                      .set.call(target, data[y]['action_args']);

                    // This will trigger a new render wor the component
                    target.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }
            target.classList.toggle('highlighting')
        }
    }
    document.removeEventListener('keydown', escaping)
    document.querySelectorAll('.highlighting').forEach((t) => t.classList.remove('highlighting'))
    yada.removeEventListener('click', nextItem)
    yada.removeAttribute('convo')
    yada.style.top = '0px'
    yada.style.left = document.body.getBoundingClientRect().width - 30 - yada.getBoundingClientRect().width + 'px'
    await delay(1000)
    yada.style.top = ''
    yada.style.left = ''
    yada_img.classList.add('sleeping')
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}