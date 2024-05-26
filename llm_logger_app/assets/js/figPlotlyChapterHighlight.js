// Immediately Invoked Function Expression (IIFE) version
(function() {
    let intervalId;

    function setupPlotlyScrollListener() {
        const figPlotly = document.getElementById('fig-plotly');

        if (figPlotly) {
            console.log('setupPlotlyScrollListener() -> Fig-plotly found, setting up listener...');
            const positionsJson = document.getElementById('fig-chapter-locations-json').textContent;
            try {
                const positions = JSON.parse(positionsJson);
                figPlotly.addEventListener('scroll', function() {
                    const currentScroll = this.scrollTop / (this.scrollHeight - this.clientHeight);
                    const chapterIndex = findCurrentChapter(currentScroll, positions.scrollRelative);
                    updateActiveChapter(chapterIndex);
                    const chapterTitle = positions.title[chapterIndex];
                    updateChapterTitle(chapterTitle);
                    console.log(`setupPlotlyScrollListener() -> ${chapterIndex} : ${chapterTitle}`);
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

        if (currentScroll < chapterStarts[0]) {
            chapterIndex = 0;
        } else if (currentScroll >= chapterStarts[chapterStarts.length-1]) {
            chapterIndex = chapterStarts.length-1;
        } else {
            for (let i = 0; i < chapterStarts.length - 1; i++) {
                if (currentScroll >= chapterStarts[i] && currentScroll < chapterStarts[i + 1]) {
                    chapterIndex = i;
                    break;
                }
            }
        }
        return chapterIndex;
    }

    function updateActiveChapter(index) {
        document.querySelectorAll('[data-type="fig-chapter-button"]').forEach((button, idx) => {
            button.className = (idx === index) ? 'fig-chapter-highlight' : 'fig-chapter';
        });
    }

    function updateChapterTitle(title) {
        var titleDiv = document.getElementById('fig-title-chapter');
        if (titleDiv) {
            titleDiv.textContent = title; // Updates the text content of the div
        } else {
            console.error('updateChapterTitle() -> No element with id "fig-title-chapter" found.');
        }
    }

    // Start the interval when everything is defined
    intervalId = setInterval(setupPlotlyScrollListener, 1000);
})();
