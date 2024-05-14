(function() {
    function setupScrollListener() {
        const targetContainer = document.getElementById('fig-index');

        if (targetContainer) {
            clearInterval(intervalId); 
            attachObserver(targetContainer);
        } else {
            console.log('setupScrollListener() -> Waiting for target container with id="fig-index"...');
        }
    }

    var intervalId = setInterval(setupScrollListener, 100);

    function attachObserver(target) {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1 && node.tagName === 'DIV' &&
                        node.getAttribute('data-type') === 'fig-chapter-button') {
                        const index = parseInt(node.getAttribute('data-index'), 10);
                        node.onclick = function() {
                            scrollToPosition(index);
                        };
                    }
                });
            });
        });

        observer.observe(target, { childList: true, subtree: true });
    }

    function scrollToPosition(index) {
        const container = document.getElementById('fig-plotly');
        const positionsJson = document.getElementById('fig-chapter-locations-json').textContent;
        const positions = JSON.parse(positionsJson);
        if (container && positions.scrollRelative.length > index) {

            // const scrollHeight = container.scrollHeight;
            // const clientHeight = container.clientHeight;
            // const scrollTopPos = scrollTop / scrollHeight;
            // const scrollMidPos = scrollTopPos + (clientHeight / scrollHeight / 2);
            const totalHeight = (container.scrollHeight - container.clientHeight);
            const offset = (container.scrollHeight / positions.scrollAbsolute[positions.scrollAbsolute.length-1]) * 0.1;
            container.scrollTop = (positions.scrollRelative[index] * totalHeight) + offset;
        }
    }
})();