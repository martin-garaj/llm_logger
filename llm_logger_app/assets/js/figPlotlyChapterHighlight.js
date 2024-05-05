// Immediately Invoked Function Expression (IIFE) version
(function() {
    let intervalId;

    function setupPlotlyScrollListener() {
        const figPlotly = document.getElementById('fig-plotly');

        if (figPlotly) {
            console.log('setupPlotlyScrollListener() -> Fig-plotly found, setting up listener...');
            const positionsJson = document.getElementById('chapter-position-json').textContent;
            try {
                const positions = JSON.parse(positionsJson);
                figPlotly.addEventListener('scroll', function() {
                    const currentScroll = this.scrollTop / (this.scrollHeight - this.clientHeight);
                    const chapterIndex = findCurrentChapter(currentScroll, positions.scroll);
                    updateActiveChapter(chapterIndex);
                });
                clearInterval(intervalId);  // Clear the interval using the locally scoped variable
                console.log('setupPlotlyScrollListener() -> Interval cleared, listener attached.');
            } catch (e) {
                console.error('setupPlotlyScrollListener() -> Error setting up scroll listener:', e);
            }
        } else {
            console.log('setupPlotlyScrollListener() -> Waiting for fig-plotly container...');
        }
    }

    function findCurrentChapter(currentScroll, chapterStarts) {
        let chapterIndex = null;
        for (let i = 0; i < chapterStarts.length - 1; i++) {
            if (currentScroll >= chapterStarts[i] && currentScroll < chapterStarts[i + 1]) {
                chapterIndex = i;
                break;
            }
        }
        if (chapterIndex === null && currentScroll >= chapterStarts[chapterStarts.length - 1]) {
            chapterIndex = chapterStarts.length - 1;
        }
        console.log(`findCurrentChapter() -> ${chapterIndex}`);
        return chapterIndex;
    }


    // Incorrectly returns chapter index, results to 'null' at the very end
    function updateActiveChapter(index) {
        document.querySelectorAll('[data-type="fig-chapter-button"]').forEach((button, idx) => {
            button.className = (idx === index) ? 'fig-chapter-highlight' : 'fig-chapter';
        });
    }

    // Start the interval when everything is defined
    intervalId = setInterval(setupPlotlyScrollListener, 1000);
})();
