// function setupScrollListener() {
//     const targetContainer = document.getElementById('fig-index');

//     if (targetContainer) {
//         clearInterval(intervalId); // Clear the interval once the container is found
//         attachObserver(targetContainer);
//     } else {
//         console.log('Waiting for target container with id="fig-index"...');
//     }
// }

// var intervalId = setInterval(setupScrollListener, 100); // Check every 100 ms

// function attachObserver(target) {
//     const observer = new MutationObserver((mutations) => {
//         mutations.forEach((mutation) => {
//             mutation.addedNodes.forEach((node) => {
//                 if (node.nodeType === 1 && node.tagName === 'DIV' &&
//                     node.getAttribute('data-type') === 'fig-chapter-button') {
//                     const index = parseInt(node.getAttribute('data-index'), 10);
//                     node.onclick = function() {
//                         scrollToPosition(index);
//                     };
//                 }
//             });
//         });
//     });

//     observer.observe(target, { childList: true, subtree: true });
// }

// function scrollToPosition(index) {
//     const container = document.getElementById('fig-plotly');
//     // for testing only
//     // const positions = [0.0, 0.1, 0.2, 0.3, 1.0]; // Example positions
//     const positionsJson = document.getElementById('chapter-position-json').textContent;
//     const positions = JSON.parse(positionsJson);
//     if (container && positions.scroll.length > index) {
//         container.scrollTop = positions.scroll[index] * (container.scrollHeight - container.clientHeight);
//     }
// }


(function() {
    function setupScrollListener() {
        const targetContainer = document.getElementById('fig-index');

        if (targetContainer) {
            clearInterval(intervalId); // Clear the interval once the container is found
            attachObserver(targetContainer);
        } else {
            console.log('setupScrollListener() -> Waiting for target container with id="fig-index"...');
        }
    }

    var intervalId = setInterval(setupScrollListener, 100); // Check every 100 ms

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
        // for testing only
        // const positions = [0.0, 0.1, 0.2, 0.3, 1.0]; // Example positions
        const positionsJson = document.getElementById('chapter-position-json').textContent;
        const positions = JSON.parse(positionsJson);
        if (container && positions.scroll.length > index) {
            container.scrollTop = positions.scroll[index] * (container.scrollHeight - container.clientHeight);
        }
    }
})();