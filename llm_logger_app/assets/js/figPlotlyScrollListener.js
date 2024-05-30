(function() {
    document.addEventListener('DOMContentLoaded', function() {
        function setupScrollListener() {
            const container = document.getElementById('fig-plotly');
            if (container) {
                clearInterval(intervalId);  // Clear the interval once the container is found
                container.onscroll = function() {
                    const scrollTop = container.scrollTop;
                    const scrollHeight = container.scrollHeight;
                    const clientHeight = container.clientHeight;
                    const scrollTopPos = scrollTop / scrollHeight;
                    const scrollMidPos = scrollTopPos + (clientHeight / scrollHeight / 2);

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

    // Initialize a local variable to hold the latest data, scoped to the IIFE
    let lastScrollData = {
        scrollTopPos: 0,
        scrollMidPos: 0
    };

    document.body.addEventListener('plotlyScroll', function(e) {
        lastScrollData = e.detail;
    });

    // Expose the scroll data function to Dash via the global dash_clientside object
    window.dash_clientside = Object.assign({}, window.dash_clientside, {
        clientside: {
            getFigScrollData: function() {
                return lastScrollData;
            }
        }
    });
})();