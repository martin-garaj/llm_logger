// function setupScrollListener() {
//     const container = document.getElementById('fig-plotly');
//     if (container) {
//         clearInterval(intervalId);  // Clear the interval once the container is found
//         container.onscroll = function() {
//             const scrollTop = container.scrollTop;
//             const scrollHeight = container.scrollHeight;
//             const clientHeight = container.clientHeight;
//             const totalHeight = scrollHeight - clientHeight;
//             const scrollPercentage = scrollTop / totalHeight;
//             const scrollTopPos = scrollTop / scrollHeight
//             const scrollMidPos = scrollTopPos + (clientHeight / scrollHeight / 2)
            
//             window.dash_clientside.callback(
//                 {output: 'fig-scroll-data.data'},
//                 [{scrollTopPos: scrollTopPos, scrollMidPos: scrollMidPos}]
//             );

//             // console.log(`Currently viewing Y-axis from ${visibleRangeStart} to ${visibleRangeEnd}`);
//             // document.getElementById('fig-title').textContent = `scrollTop=${Number(scrollTop).toFixed(1)} scrollHeight=${Number(scrollHeight).toFixed(1)} clientHeight=${Number(clientHeight).toFixed(1)} totalHeight=${Number(totalHeight).toFixed(1)} scrollPercentage=${Number(scrollPercentage).toFixed(1)}`;
//             document.getElementById('fig-title').textContent = `scrollTopPos=${Number(scrollTopPos).toFixed(2)} scrollMidPos=${Number(scrollMidPos).toFixed(2)}`;
//             // document.getElementById('fig-title').textContent = `scrollTopPos=${Number(scrollTopPos).toFixed(2)} scrollMidPos=${Number(scrollMidPos).toFixed(2)}`;
//         };
//     }
// }

// var intervalId = setInterval(setupScrollListener, 100);  // Check every 100 ms




document.addEventListener('DOMContentLoaded', function() {
    function setupScrollListener() {
        const container = document.getElementById('fig-plotly');
        if (container) {
            clearInterval(intervalId);
            container.onscroll = function() {
                const scrollTop = container.scrollTop;
                const scrollHeight = container.scrollHeight;
                const clientHeight = container.clientHeight;
                const scrollTopPos = scrollTop / scrollHeight;
                const scrollMidPos = scrollTopPos + (clientHeight / scrollHeight / 2);

                // Use document body to dispatch the event to ensure it can be globally accessed
                document.body.dispatchEvent(new CustomEvent('plotlyScroll', {
                    detail: {
                        scrollTopPos: scrollTopPos,
                        scrollMidPos: scrollMidPos
                    }
                }));
            };
        }
    }

    var intervalId = setInterval(setupScrollListener, 100);
});


/////////////////////   JavaScript file to provide the latest event data to Dash
// Assuming a global variable to hold the latest data
let lastScrollData = {
    scrollTopPos: 0,
    scrollMidPos: 0
};

document.body.addEventListener('plotlyScroll', function(e) {
    lastScrollData = e.detail;
});

// Function to be called by Dash's clientside callback
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        getFigScrollData: function() {
            return lastScrollData;
        }
    }
});
