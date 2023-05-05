function escaping() {
    if (event.key == 'Escape' || event.which == 27 || event.code == 'Escape') {
        escaped = true
        paused = false
    }}

function nextItem() {paused = false}

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
                if (data[y]['action'] == 'click') {target.dispatchEvent(new MouseEvent("click"))}
                if (data[y]['action'] == 'dblclick') {target.dispatchEvent(new MouseEvent("dblclick"))}
                if (data[y]['action'] == 'send_keys') {
                    target.send_keys(data[y]['action_args'])
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