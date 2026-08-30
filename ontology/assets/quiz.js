/* ============================================================
   quiz.js — shared lesson quiz widget (Ontology course)
   Markup contract:
     <div class="quiz">
       <p class="quiz-q">Question…</p>
       <div class="quiz-opts">
         <button class="opt" data-correct="true">Option A</button>
         <button class="opt">Option B</button>
         <button class="opt">Option C</button>
       </div>
       <p class="quiz-fb" hidden></p>
     </div>
   On click: locks options, marks correct/wrong, reveals feedback
   with a tight, immediate loop. All feedback text lives in the
   button's data-fb or a shared data-fb on the .quiz container.
   ============================================================ */
(function () {
  function bindOne(quiz) {
    var opts = quiz.querySelectorAll('button.opt');
    var fb = quiz.querySelector('.quiz-fb');
    var answered = false;

    function reveal(correct, button) {
      answered = true;
      opts.forEach(function (b) { b.disabled = true; });
      opts.forEach(function (b) { b.classList.remove('correct', 'wrong'); });
      if (button) button.classList.add(correct ? 'correct' : 'wrong');
      // also highlight the true correct answer if the choice was wrong
      if (!correct) {
        opts.forEach(function (b) {
          if (b.getAttribute('data-correct') === 'true') b.classList.add('correct');
        });
      }
      if (fb) {
        var extra = button && button.getAttribute('data-fb');
        var base = quiz.getAttribute('data-fb');
        fb.textContent = extra || base || '';
        fb.hidden = false;
        fb.className = 'quiz-fb ' + (correct ? 'correct' : 'wrong');
      }
    }

    opts.forEach(function (button) {
      button.addEventListener('click', function () {
        if (answered) return;
        reveal(button.getAttribute('data-correct') === 'true', button);
      });
    });
  }

  function init() {
    document.querySelectorAll('.quiz').forEach(bindOne);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
