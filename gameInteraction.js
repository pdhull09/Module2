$(document).ready(function() {
    let isDragging = false;
    let startX, startY;
    let line = null; // Initialize line as null

    // Function to load SVG content
    function loadSVGContent() {
        const url = /svgs/table_${currentTableId}.svg;
        $.ajax({
            url: url,
            type: "GET",
            dataType: "text",
            success: function(svgData) {
                $("#svgContainer").html(svgData);

                // After SVG is loaded, find the cue ball within the SVG
                const cueBall = $("#svgContainer").find('circle[fill="WHITE"]');

                // Mouse down event on cue ball
                $("#svgContainer").on('mousedown','circle[fill="WHITE"]', function(event) {
                    isDragging = true;
                    startX = event.clientX;
                    startY = event.clientY;
                    const cueBallX = parseFloat(cueBall.attr("cx"));
                    const cueBallY = parseFloat(cueBall.attr("cy"));

                    const svgNS = "http://www.w3.org/2000/svg";
                    line = document.createElementNS(svgNS, 'line');
                    line.setAttribute("x1", cueBallX);
                    line.setAttribute("y1", cueBallY);
                    line.setAttribute("stroke", "black");
                    line.setAttribute("stroke-width", "5");
                    $('#svgContainer svg').append(line);
                });

                // Mouse move event on document to track dragging
                $(document).mousemove(function(event) {
                    if (isDragging && line !== null) {
                        line.setAttribute("x2", event.clientX);
                        line.setAttribute("y2", event.clientY);
                    }
                });

                // Mouse up event on document to end dragging
                $(document).mouseup(function(event) {
                    if (isDragging && line !== null) {
                        isDragging = false;
                        const deltaX = event.clientX - startX;
                        const deltaY = event.clientY - startY;

                        $(line).remove(); // Remove the line
                        line = null; // Reset line to null

                        // Process the shot with the calculated deltaX and deltaY
                        processShot(deltaX, deltaY);
                    }
                });
            }
        });
    }

    // Function to process the shot and send data to the server
    function processShot(deltaX, deltaY) {
        // Convert deltas to velocity or any other required format
        const data = { deltaX, deltaY };
        $.ajax({
            url: '/processShot',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                console.log('Shot processed:', response);
                // Reload SVG content if needed
                loadSVGContent();
            },
            error: function(xhr, status, error) {
                console.error('Error processing shot:', error);
            }
        });
    }

    // Initial load of SVG content
    loadSVGContent();
});
