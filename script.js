const RANDOM_QUOTE_API_URL = 'http://api.quotable.io/random'
const quoteDisplayElement = document.getElementById('quoteDisplay')
const quoteInputElement = document.getElementById('quoteInput')
const timerElement = document.getElementById('timer')
const testLength = document.getElementById('testLength')

let typedCharacters = 0
let correctCharacters = 0
let incorrectCharacters = 0
let wpm = 0

quoteInputElement.addEventListener('input', () => {
  const arrayQuote = quoteDisplayElement.querySelectorAll('span')
  const arrayValue = quoteInputElement.value.split('')

  let correct = true
  arrayQuote.forEach((characterSpan, index) => {
    const character = arrayValue[index]
    if (character == null) {
      characterSpan.classList.remove('correct')
      characterSpan.classList.remove('incorrect')
      correct = false
    } else if (character === characterSpan.innerText) {
      characterSpan.classList.add('correct')
      characterSpan.classList.remove('incorrect')
    } else {
      characterSpan.classList.remove('correct')
      characterSpan.classList.add('incorrect')
      correct = false

    }
})

if (correct) renderNewQuote()
typedCharacters += 1
typedWords = typedCharacters / 5
wpm = typedWords / parseInt(testLength.innerText)

})


async function getRandomQuote() {
  const response = await fetch(RANDOM_QUOTE_API_URL)
    const data = await response.json()
    return data.content
}

async function renderNewQuote() {
  const quote = await getRandomQuote()
  quoteDisplayElement.innerHTML = ''
  quote.split('').forEach(character => {
    const characterSpan = document.createElement('span')
    characterSpan.innerText = character
    quoteDisplayElement.appendChild(characterSpan)
  })
  quoteInputElement.value = null
//   startTimer()
}


let startTime
let timeStarted = false
function startTimer() {
    if (timeStarted == false) {
        timerElement.innerText = 0
        setInterval(() => {
            if (parseInt(timerElement.innerText) < parseInt(testLength.innerText) * 60)
            {
                timer.innerText = getTimerTime()
            }
            else
            {
                timerElement.innerText = "TIMES UP!"
                quoteInputElement.disabled = true
                document.getElementById('invisibleForm').value=wpm
                document.forms[0].submit()
            }
        }, 1000)
        startTime = new Date()
        timeStarted = true
    }
}

function getTimerTime() {
  return Math.floor((new Date() - startTime) / 1000)
}

window.addEventListener('keydown', function() {
    document.getElementById("quoteInput").focus()
    startTimer()
});


// if (parseInt(timerElement.innerText) > parseInt(testLength.innerText) * 60) {
//     timerElement.innerText = "TIMES UP!"
// }

renderNewQuote()