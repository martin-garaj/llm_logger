(function() {
    let intervalId = setInterval(() => {
        const figGraph = document.getElementById('fig-graph');
        if (figGraph) {
            // clearInterval(intervalId);
            adjustGraphSize();
        } else {
            console.log('figPlotlyResize -> Waiting for fig-graph to load fully...');
        }
    }, 1000); // Check every second

    function adjustGraphSize() {
        // sanity check
        const figPlotly = document.getElementById('fig-plotly');
        if (!figPlotly) {
            console.log('adjustGraphSize() -> fig-plotly is not available');
            return;
        }
        const divAspectRatio = document.getElementById('fig-graph-aspect-ratio');
        if (!divAspectRatio) {
            console.log('adjustGraphSize() -> "fig-graph-aspect-ratio" is not available');
            return;
        }
        // checked before the function is called
        const figGraph = document.getElementById('fig-graph');
        // if (!figGraph) {
        //     console.log('adjustGraphSize() -> "fig-graph" is not available');
        //     return;
        // }

        // recalculate dimensions
        aspect_ratio = parseFloat(divAspectRatio.textContent);
        const width = figPlotly.clientWidth; 
        const height = parseInt(width * aspect_ratio); 

        // update dimensions only if they differ
        if ((figGraph.style.width.localeCompare(`${width}px`) == 0) && (figGraph.style.height.localeCompare(`${height}px`) == 0)) {
            return;
        } else {
            console.log(`adjustGraphSize() -> width=${width}px, height=${height}px, aspect_ratio=${aspect_ratio}`);
            figGraph.style.width = `${width}px`;
            figGraph.style.height = `${height}px`;
        }
    }
})();

// (function() {
//     document.addEventListener('DOMContentLoaded', function() {
//         const figPlotly = document.getElementById('fig-plotly');
//         const figGraph = document.getElementById('fig-graph');
//         let intervalId = null; // Initialize the interval ID

//         console.log('adjustGraphSize() -> Listener being added.');

//         function adjustGraphSize() {
//             if (figPlotly) {
//                 console.log('adjustGraphSize() -> Waiting for fig-plotly IS available');
//             } else {
//                 console.log('adjustGraphSize() -> Waiting for fig-plotly IS NOT available');
//             }

//             if (figGraph) {
//                 console.log('adjustGraphSize() -> Waiting for fig-graph IS available');
//             } else {
//                 console.log('adjustGraphSize() -> Waiting for fig-graph IS NOT available');
//             }

//             if (figPlotly && figGraph) {
//                 let width = figPlotly.clientWidth; // Get the current width
//                 let height = width * 10; // (desiredHeight / desiredWidth); // Calculate height based on aspect ratio

//                 // Set the dimensions
//                 figGraph.style.width = `${width}px`;
//                 figGraph.style.height = `${height}px`;

//                 if (width > 0) { // Assuming width > 0 as a condition that the graph is loaded
//                     clearInterval(intervalId); // Clear the interval once the figure is properly adjusted
//                     console.log('adjustGraphSize() -> Interval cleared, graph size adjusted.');
//                 }
//             } else {
//                 console.log('adjustGraphSize() -> Waiting for fig-plotly or fig-graph to be available...');
//             }
//         }

//         // Initial adjustment might not work if the graph isn't fully rendered, so set up an interval
//         intervalId = setInterval(adjustGraphSize, 1000);

//         // Also adjust on window resize
//         window.addEventListener('resize', adjustGraphSize);
//     });
// })();