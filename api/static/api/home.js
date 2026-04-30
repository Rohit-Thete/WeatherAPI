(function () {
    const configElement = document.getElementById("app-config");

    if (!configElement) {
        return;
    }

    const config = JSON.parse(configElement.textContent);
    const datasets = config.datasets;
    const state = {
        activeDataset: "monthly",
        nextPage: null,
        previousPage: null,
    };

    const filterForm = document.getElementById("filter-form");
    const createForm = document.getElementById("create-form");
    const datasetSwitch = document.getElementById("dataset-switch");
    const summary = document.getElementById("results-summary");
    const averageValue = document.getElementById("average-value");
    const averageMeta = document.getElementById("average-meta");
    const tableHead = document.getElementById("results-head");
    const tableBody = document.getElementById("results-body");
    const chartTitle = document.getElementById("chart-title");
    const chartBadge = document.getElementById("chart-badge");
    const trendCaption = document.getElementById("trend-caption");
    const comparisonCaption = document.getElementById("comparison-caption");
    const trendChart = document.getElementById("trend-chart");
    const comparisonChart = document.getElementById("comparison-chart");
    const trendTooltip = document.getElementById("trend-tooltip");
    const comparisonTooltip = document.getElementById("comparison-tooltip");
    const previousButton = document.getElementById("previous-page");
    const nextButton = document.getElementById("next-page");
    const resetButton = document.getElementById("reset-filters");
    const submitStatus = document.getElementById("submit-status");
    const createResponse = document.getElementById("create-response");

    const explorerPeriodFields = {
        month: document.getElementById("filter-month-field"),
        season: document.getElementById("filter-season-field"),
    };
    const composerPeriodFields = {
        month: document.getElementById("create-month-field"),
        season: document.getElementById("create-season-field"),
    };
    const statsElements = {
        monthly: document.getElementById("stat-monthly"),
        seasonal: document.getElementById("stat-seasonal"),
        annual: document.getElementById("stat-annual"),
    };
    const monthOrder = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ];
    const seasonOrder = ["winter", "spring", "summer", "autumn"];

    function setExplorerDataset(datasetName) {
        state.activeDataset = datasetName;

        datasetSwitch.querySelectorAll("[data-dataset]").forEach((button) => {
            button.classList.toggle("is-active", button.dataset.dataset === datasetName);
        });

        chartBadge.textContent = datasetName;
        chartTitle.textContent = `${datasets[datasetName].label} trends`;
        togglePeriodFields(explorerPeriodFields, datasetName, filterForm);
        renderTableHeader(datasetName);
    }

    function togglePeriodFields(fields, datasetName, form) {
        const dataset = datasets[datasetName];
        const showMonth = dataset.periodField === "month";
        const showSeason = dataset.periodField === "season";

        fields.month.classList.toggle("is-hidden", !showMonth);
        fields.season.classList.toggle("is-hidden", !showSeason);

        if (!showMonth && form.elements.month) {
            form.elements.month.value = "";
        }

        if (!showSeason && form.elements.season) {
            form.elements.season.value = "";
        }
    }

    function renderTableHeader(datasetName) {
        const columns = datasets[datasetName].columns;
        tableHead.innerHTML =
            "<tr>" +
            columns.map((column) => `<th scope="col">${column.label}</th>`).join("") +
            "</tr>";
    }

    function renderTableRows(datasetName, rows) {
        const columns = datasets[datasetName].columns;

        if (!rows.length) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="${columns.length}">No records matched this query.</td>
                </tr>
            `;
            return;
        }

        tableBody.innerHTML = rows
            .map((row) => {
                const cells = columns
                    .map((column) => `<td>${escapeHtml(row[column.key])}</td>`)
                    .join("");
                return `<tr>${cells}</tr>`;
            })
            .join("");
    }

    function escapeHtml(value) {
        return String(value ?? "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#39;");
    }

    function buildFilterUrl(datasetName) {
        const params = new URLSearchParams();
        const formData = new FormData(filterForm);
        const dataset = datasets[datasetName];

        for (const [key, value] of formData.entries()) {
            if (!value) {
                continue;
            }

            if ((key === "month" || key === "season") && key !== dataset.periodField) {
                continue;
            }

            params.set(key, value);
        }

        const query = params.toString();
        return query ? `${dataset.endpoint}?${query}` : dataset.endpoint;
    }

    async function readResponse(response) {
        const contentType = response.headers.get("content-type") || "";

        if (contentType.includes("application/json")) {
            return response.json();
        }

        return response.text();
    }

    async function fetchRecords(url) {
        summary.textContent = `Loading ${state.activeDataset} records...`;
        averageValue.textContent = "Loading...";
        averageMeta.textContent = "Calculating page average";
        trendCaption.textContent = "Loading trend graph...";
        comparisonCaption.textContent = "Loading comparison graph...";

        const response = await fetch(url, {
            headers: {
                Accept: "application/json",
            },
        });
        const payload = await readResponse(response);

        if (!response.ok) {
            throw new Error(typeof payload === "string" ? payload : JSON.stringify(payload));
        }

        state.nextPage = payload.next;
        state.previousPage = payload.previous;
        previousButton.disabled = !payload.previous;
        nextButton.disabled = !payload.next;

        renderTableRows(state.activeDataset, payload.results || []);
        renderCharts(state.activeDataset, payload.results || []);

        const shownCount = payload.results ? payload.results.length : 0;
        summary.textContent = `Showing ${shownCount} of ${payload.count} ${state.activeDataset} records.`;
        updateAverageMetric(payload.results || []);
    }

    async function runExplorer(url) {
        try {
            await fetchRecords(url);
        } catch (error) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="${datasets[state.activeDataset].columns.length}">Unable to load records.</td>
                </tr>
            `;
            summary.textContent = "Request failed.";
            averageValue.textContent = "Unavailable";
            averageMeta.textContent = "Could not calculate average";
            renderChartMessage(trendChart, "Unable to render the trend graph.");
            renderChartMessage(comparisonChart, "Unable to render the comparison graph.");
            hideTooltip(trendChart, trendTooltip);
            hideTooltip(comparisonChart, comparisonTooltip);
            trendCaption.textContent = error.message;
            comparisonCaption.textContent = "Try adjusting filters or retrying the request.";
            previousButton.disabled = true;
            nextButton.disabled = true;
        }
    }

    function getCsrfToken() {
        const tokenInput = createForm.querySelector("[name=csrfmiddlewaretoken]");
        return tokenInput ? tokenInput.value : "";
    }

    function updateStatus(message, stateName) {
        submitStatus.textContent = message;
        submitStatus.dataset.state = stateName;
    }

    async function refreshStats() {
        const entries = Object.entries(datasets);

        await Promise.all(
            entries.map(async ([datasetName, dataset]) => {
                const response = await fetch(dataset.endpoint, {
                    headers: {
                        Accept: "application/json",
                    },
                });
                const payload = await readResponse(response);

                if (response.ok && typeof payload.count === "number" && statsElements[datasetName]) {
                    statsElements[datasetName].textContent = payload.count;
                }
            })
        );
    }

    function addRegionSuggestion(regionName) {
        if (!regionName) {
            return;
        }

        const datalist = document.getElementById("region-options");
        const alreadyExists = Array.from(datalist.options).some(
            (option) => option.value === regionName
        );

        if (alreadyExists) {
            return;
        }

        const option = document.createElement("option");
        option.value = regionName;
        datalist.appendChild(option);
    }

    function updateAverageMetric(rows) {
        if (!rows.length) {
            averageValue.textContent = "No data";
            averageMeta.textContent = "Run a query with matching records";
            return;
        }

        const parameters = [...new Set(rows.map((row) => row.parameter))];
        const units = [...new Set(rows.map((row) => row.unit).filter(Boolean))];

        if (parameters.length !== 1 || units.length !== 1) {
            averageValue.textContent = "Filter first";
            averageMeta.textContent = "Choose one parameter to get a meaningful average";
            return;
        }

        const total = rows.reduce((sum, row) => sum + Number(row.value), 0);
        const average = total / rows.length;

        averageValue.textContent = `${average.toFixed(2)} ${units[0]}`;
        averageMeta.textContent = `${rows.length} records for ${parameters[0]} on this page`;
    }

    function setChartTargetActive(chartElement, activeTarget) {
        chartElement.querySelectorAll(".chart-target").forEach((target) => {
            target.classList.toggle("is-active", target === activeTarget);
        });
    }

    function positionTooltip(chartElement, tooltipElement, anchorX, anchorY) {
        const chartFrame = chartElement.closest(".chart-frame");
        const frameRect = chartFrame.getBoundingClientRect();
        const tooltipWidth = tooltipElement.offsetWidth;
        const tooltipHeight = tooltipElement.offsetHeight;
        let left = anchorX - tooltipWidth / 2;
        let top = anchorY - tooltipHeight - 14;

        left = Math.max(8, Math.min(left, frameRect.width - tooltipWidth - 8));

        if (top < 8) {
            top = anchorY + 14;
        }

        tooltipElement.style.left = `${left}px`;
        tooltipElement.style.top = `${top}px`;
    }

    function showTooltip(chartElement, tooltipElement, target, anchorPosition) {
        tooltipElement.innerHTML = `
            <span class="chart-tooltip-title">${escapeHtml(target.dataset.title || "")}</span>
            <span class="chart-tooltip-value">${escapeHtml(target.dataset.value || "")}</span>
            <span class="chart-tooltip-meta">${escapeHtml(target.dataset.meta || "")}</span>
        `;
        tooltipElement.classList.remove("is-hidden");
        tooltipElement.classList.add("is-visible");
        tooltipElement.setAttribute("aria-hidden", "false");
        positionTooltip(chartElement, tooltipElement, anchorPosition.x, anchorPosition.y);
    }

    function hideTooltip(chartElement, tooltipElement) {
        setChartTargetActive(chartElement, null);
        tooltipElement.classList.add("is-hidden");
        tooltipElement.classList.remove("is-visible");
        tooltipElement.setAttribute("aria-hidden", "true");
    }

    function getSvgAnchorPosition(chartElement, svgX, svgY) {
        const viewBox = chartElement.viewBox.baseVal;
        const chartRect = chartElement.getBoundingClientRect();
        const frameRect = chartElement.closest(".chart-frame").getBoundingClientRect();

        return {
            x: ((svgX - viewBox.x) / viewBox.width) * chartRect.width + (chartRect.left - frameRect.left),
            y:
                ((svgY - viewBox.y) / viewBox.height) * chartRect.height +
                (chartRect.top - frameRect.top),
        };
    }

    function attachChartInteractions(chartElement, tooltipElement) {
        chartElement.querySelectorAll(".chart-target").forEach((target) => {
            target.addEventListener("pointerenter", (event) => {
                const frameRect = chartElement.closest(".chart-frame").getBoundingClientRect();
                setChartTargetActive(chartElement, target);
                showTooltip(chartElement, tooltipElement, target, {
                    x: event.clientX - frameRect.left,
                    y: event.clientY - frameRect.top,
                });
            });

            target.addEventListener("pointermove", (event) => {
                const frameRect = chartElement.closest(".chart-frame").getBoundingClientRect();
                showTooltip(chartElement, tooltipElement, target, {
                    x: event.clientX - frameRect.left,
                    y: event.clientY - frameRect.top,
                });
            });

            target.addEventListener("pointerleave", () => {
                hideTooltip(chartElement, tooltipElement);
            });

            target.addEventListener("focus", () => {
                const position = getSvgAnchorPosition(
                    chartElement,
                    Number(target.dataset.anchorX),
                    Number(target.dataset.anchorY)
                );

                setChartTargetActive(chartElement, target);
                showTooltip(chartElement, tooltipElement, target, position);
            });

            target.addEventListener("blur", () => {
                hideTooltip(chartElement, tooltipElement);
            });

            target.addEventListener("keydown", (event) => {
                if (event.key === "Escape") {
                    hideTooltip(chartElement, tooltipElement);
                    target.blur();
                }
            });
        });
    }

    function renderChartMessage(chartElement, message) {
        chartElement.innerHTML = `
            <text x="50%" y="50%" text-anchor="middle" class="chart-empty-text">${escapeHtml(
                message
            )}</text>
        `;
    }

    function getSortedRows(datasetName, rows) {
        return [...rows].sort((left, right) => {
            if (left.year !== right.year) {
                return Number(left.year) - Number(right.year);
            }

            if (datasetName === "monthly") {
                return monthOrder.indexOf(left.month) - monthOrder.indexOf(right.month);
            }

            if (datasetName === "seasonal") {
                return seasonOrder.indexOf(left.season) - seasonOrder.indexOf(right.season);
            }

            return String(left.region).localeCompare(String(right.region));
        });
    }

    function getPrimaryLabel(datasetName, row) {
        if (datasetName === "annual") {
            return String(row.year);
        }

        if (datasetName === "seasonal") {
            return `${row.year} ${titleCase(row.season)}`;
        }

        return `${row.year} ${titleCase(row.month).slice(0, 3)}`;
    }

    function titleCase(value) {
        return String(value ?? "")
            .split("_")
            .map((part) => {
                if (!part) {
                    return part;
                }

                if (part === part.toUpperCase()) {
                    return part;
                }

                return part.charAt(0).toUpperCase() + part.slice(1);
            })
            .join(" ");
    }

    function renderCharts(datasetName, rows) {
        const sortedRows = getSortedRows(datasetName, rows);

        if (!sortedRows.length) {
            renderChartMessage(trendChart, "No filtered records to plot.");
            renderChartMessage(comparisonChart, "No filtered records to compare.");
            hideTooltip(trendChart, trendTooltip);
            hideTooltip(comparisonChart, comparisonTooltip);
            trendCaption.textContent = "Run a filter query with matching records to see the trend line.";
            comparisonCaption.textContent =
                "The comparison graph will appear once the current page has data.";
            return;
        }

        renderTrendChart(datasetName, sortedRows);
        renderComparisonChart(datasetName, sortedRows);
        attachChartInteractions(trendChart, trendTooltip);
        attachChartInteractions(comparisonChart, comparisonTooltip);
    }

    function renderTrendChart(datasetName, rows) {
        const width = 480;
        const height = 240;
        const padding = { top: 24, right: 18, bottom: 46, left: 44 };
        const values = rows.map((row) => Number(row.value));
        const minValue = Math.min(...values);
        const maxValue = Math.max(...values);
        const scaleMin = maxValue === minValue ? minValue - 1 : minValue;
        const scaleMax = maxValue === minValue ? maxValue + 1 : maxValue;
        const range = scaleMax - scaleMin;
        const innerWidth = width - padding.left - padding.right;
        const innerHeight = height - padding.top - padding.bottom;
        const stepX = rows.length > 1 ? innerWidth / (rows.length - 1) : 0;
        const points = rows.map((row, index) => {
            const x =
                rows.length > 1 ? padding.left + stepX * index : padding.left + innerWidth / 2;
            const normalized = (Number(row.value) - scaleMin) / range;
            const y = padding.top + innerHeight - normalized * innerHeight;

            return {
                x,
                y,
                label: getPrimaryLabel(datasetName, row),
                value: Number(row.value),
                row,
            };
        });
        const linePath = points
            .map((point, index) => `${index === 0 ? "M" : "L"} ${point.x} ${point.y}`)
            .join(" ");
        const areaPath =
            `${linePath} L ${points[points.length - 1].x} ${height - padding.bottom} ` +
            `L ${points[0].x} ${height - padding.bottom} Z`;
        const gridValues = Array.from(
            { length: 4 },
            (_, index) => scaleMin + (range / 3) * index
        );
        const gridMarkup = gridValues
            .map((value) => {
                const normalized = (value - scaleMin) / range;
                const y = padding.top + innerHeight - normalized * innerHeight;
                return `
                    <line class="chart-grid-line" x1="${padding.left}" y1="${y}" x2="${
                    width - padding.right
                }" y2="${y}"></line>
                    <text class="chart-axis-label" x="${padding.left - 8}" y="${y + 4}" text-anchor="end">${value.toFixed(
                    1
                )}</text>
                `;
            })
            .join("");
        const labelStep = points.length > 6 ? Math.ceil(points.length / 6) : 1;
        const labelMarkup = points
            .map((point, index) => {
                if (index % labelStep !== 0 && index !== points.length - 1) {
                    return "";
                }

                return `
                    <text class="chart-axis-label" x="${point.x}" y="${
                    height - 20
                }" text-anchor="middle">${escapeHtml(shortLabel(point.label))}</text>
                `;
            })
            .join("");
        const dotMarkup = points
            .map((point) => {
                const meta = `${titleCase(point.row.region)} | ${point.row.parameter}`;
                const valueText = `${point.value.toFixed(2)} ${point.row.unit || ""}`.trim();

                return `
                    <g
                        class="chart-target chart-point"
                        tabindex="0"
                        role="img"
                        aria-label="${escapeHtml(`${point.label}: ${valueText}. ${meta}`)}"
                        data-title="${escapeHtml(point.label)}"
                        data-value="${escapeHtml(valueText)}"
                        data-meta="${escapeHtml(meta)}"
                        data-anchor-x="${point.x}"
                        data-anchor-y="${point.y}"
                    >
                        <circle class="chart-hit-ring" cx="${point.x}" cy="${point.y}" r="14"></circle>
                        <circle class="chart-dot" cx="${point.x}" cy="${point.y}" r="4"></circle>
                    </g>
                `;
            })
            .join("");

        trendChart.innerHTML = `
            <defs>
                <linearGradient id="trendFill" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%" stop-color="rgba(79, 124, 255, 0.32)"></stop>
                    <stop offset="100%" stop-color="rgba(79, 124, 255, 0.04)"></stop>
                </linearGradient>
            </defs>
            ${gridMarkup}
            <line class="chart-axis-line" x1="${padding.left}" y1="${height - padding.bottom}" x2="${
            width - padding.right
        }" y2="${height - padding.bottom}"></line>
            <path class="chart-area" d="${areaPath}"></path>
            <path class="chart-line" d="${linePath}"></path>
            ${dotMarkup}
            ${labelMarkup}
        `;

        const periodName =
            datasetName === "annual"
                ? "year"
                : datasetName === "seasonal"
                  ? "season"
                  : "month";
        trendCaption.textContent = `Hover or tab through points to inspect values across the ${rows.length} records ordered by ${periodName}.`;
    }

    function getComparisonGrouping(datasetName, rows) {
        const uniqueRegions = new Set(rows.map((row) => row.region));
        const uniqueParameters = new Set(rows.map((row) => row.parameter));

        if (uniqueRegions.size > 1) {
            return { key: "region", label: "region" };
        }

        if (uniqueParameters.size > 1) {
            return { key: "parameter", label: "parameter" };
        }

        if (datasetName === "monthly") {
            return { key: "month", label: "month" };
        }

        if (datasetName === "seasonal") {
            return { key: "season", label: "season" };
        }

        return { key: "year", label: "year" };
    }

    function renderComparisonChart(datasetName, rows) {
        const grouping = getComparisonGrouping(datasetName, rows);
        const grouped = new Map();

        rows.forEach((row) => {
            const key = String(row[grouping.key]);
            const current = grouped.get(key) || { total: 0, count: 0 };
            current.total += Number(row.value);
            current.count += 1;
            grouped.set(key, current);
        });

        const items = [...grouped.entries()]
            .map(([label, stats]) => ({
                label,
                value: stats.total / stats.count,
            }))
            .sort((left, right) => right.value - left.value)
            .slice(0, 6);

        if (!items.length) {
            renderChartMessage(comparisonChart, "No comparison data available.");
            comparisonCaption.textContent = "Try broadening the filters to compare values.";
            return;
        }

        const width = 480;
        const height = 220;
        const padding = { top: 18, right: 16, bottom: 20, left: 110 };
        const innerWidth = width - padding.left - padding.right;
        const barHeight = 18;
        const barGap = 14;
        const maxValue = Math.max(...items.map((item) => item.value)) || 1;

        const barMarkup = items
            .map((item, index) => {
                const y = padding.top + index * (barHeight + barGap);
                const barWidth = (item.value / maxValue) * innerWidth;
                const label = titleCase(item.label);
                const valueText = `${item.value.toFixed(2)} average`;

                return `
                    <g
                        class="chart-target chart-bar-group"
                        tabindex="0"
                        role="img"
                        aria-label="${escapeHtml(`${label}: ${valueText}`)}"
                        data-title="${escapeHtml(label)}"
                        data-value="${escapeHtml(valueText)}"
                        data-meta="${escapeHtml(`Grouped by ${grouping.label}`)}"
                        data-anchor-x="${padding.left + barWidth}"
                        data-anchor-y="${y + barHeight / 2}"
                    >
                        <text class="chart-axis-label" x="${padding.left - 10}" y="${
                    y + 12
                }" text-anchor="end">${escapeHtml(shortLabel(label, 14))}</text>
                        <rect class="chart-hit-bar" x="${padding.left}" y="${y - 4}" width="${Math.max(
                    barWidth,
                    10
                )}" height="${barHeight + 8}" rx="11"></rect>
                        <rect class="chart-bar" x="${padding.left}" y="${y}" width="${barWidth}" height="${barHeight}" rx="9"></rect>
                        <text class="chart-value-label" x="${padding.left + barWidth + 8}" y="${
                    y + 13
                }">${item.value.toFixed(1)}</text>
                    </g>
                `;
            })
            .join("");

        comparisonChart.innerHTML = `
            <defs>
                <linearGradient id="barFill" x1="0" x2="1" y1="0" y2="0">
                    <stop offset="0%" stop-color="#4f7cff"></stop>
                    <stop offset="100%" stop-color="#1fbad6"></stop>
                </linearGradient>
            </defs>
            ${barMarkup}
        `;

        comparisonCaption.textContent = `Hover or tab through bars to compare the page average grouped by ${grouping.label}.`;
    }

    function shortLabel(value, limit = 10) {
        const text = String(value);
        if (text.length <= limit) {
            return text;
        }

        return `${text.slice(0, Math.max(limit - 3, 1))}...`;
    }

    async function submitRecord(event) {
        event.preventDefault();

        const datasetName = createForm.elements.dataset.value;
        const dataset = datasets[datasetName];
        const payload = {
            year: Number(createForm.elements.year.value),
            region: createForm.elements.region.value.trim(),
            parameter: createForm.elements.parameter.value,
            value: Number(createForm.elements.value.value),
        };

        if (dataset.periodField === "month") {
            payload.month = createForm.elements.month.value;
        }

        if (dataset.periodField === "season") {
            payload.season = createForm.elements.season.value;
        }

        updateStatus(`Sending ${datasetName} record...`, "idle");

        const response = await fetch(dataset.endpoint, {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken(),
            },
            body: JSON.stringify(payload),
        });

        const responsePayload = await readResponse(response);
        createResponse.textContent = JSON.stringify(responsePayload, null, 2);

        if (!response.ok) {
            updateStatus("The API rejected this record. Check the response details below.", "error");
            return;
        }

        updateStatus(`${dataset.label} record saved successfully.`, "success");
        addRegionSuggestion(responsePayload.region || payload.region);
        await refreshStats();

        if (datasetName === state.activeDataset) {
            await runExplorer(buildFilterUrl(state.activeDataset));
        }
    }

    datasetSwitch.addEventListener("click", (event) => {
        const button = event.target.closest("[data-dataset]");

        if (!button) {
            return;
        }

        setExplorerDataset(button.dataset.dataset);
        runExplorer(buildFilterUrl(state.activeDataset));
    });

    filterForm.addEventListener("submit", (event) => {
        event.preventDefault();
        runExplorer(buildFilterUrl(state.activeDataset));
    });

    resetButton.addEventListener("click", () => {
        filterForm.reset();
        togglePeriodFields(explorerPeriodFields, state.activeDataset, filterForm);
        runExplorer(buildFilterUrl(state.activeDataset));
    });

    previousButton.addEventListener("click", () => {
        if (state.previousPage) {
            runExplorer(state.previousPage);
        }
    });

    nextButton.addEventListener("click", () => {
        if (state.nextPage) {
            runExplorer(state.nextPage);
        }
    });

    createForm.elements.dataset.addEventListener("change", (event) => {
        togglePeriodFields(composerPeriodFields, event.target.value, createForm);
    });

    createForm.addEventListener("submit", (event) => {
        submitRecord(event).catch((error) => {
            updateStatus("The request failed before the API could respond.", "error");
            createResponse.textContent = error.message;
        });
    });

    setExplorerDataset(state.activeDataset);
    togglePeriodFields(composerPeriodFields, createForm.elements.dataset.value, createForm);
    runExplorer(buildFilterUrl(state.activeDataset));
})();

