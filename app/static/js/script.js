// Constants

const CONTENT_WIDTH = 640;
const CONTENT_HEIGHT = 910;

// Cell value converters

function toCellValue(s) {
    return (s == "") ? null : parseInt(s);
}

function toCellNum(s) {
    return (s == "") ? "0" : s;
}

function fromCellValue(v) {
    return (v === null) ? "" : v.toString();
}


// Style uitls

function setStyles(element, styles) {
    Object.assign(element.style, styles);
}


// Notification utils

function notify(text) {
    document.getElementById("notification").textContent = text;
    document.getElementById("notify-bar__content").setAttribute('title', text);
    const bar = document.getElementById("notify-bar")
    setStyles(bar, {
        opacity: 1.0,
        top: 0
    })
}

function hideNotification() {
    const bar = document.getElementById("notify-bar");
    setStyles(bar, {
        opacity: 0.0,
        top: -bar.offsetHeight + "px"
    })
}


// Grid manipulation utils

function getGrid() {
    return Array.from(
        Array(9).keys(),
        i => Array.from(
            Array(9).keys(),
            j => toCellValue(document.getElementById(`Cell(${i},${j})`).value)
        )
    );
}

function getStringifiedGrid() {
    return Array.from(
        Array(81).keys(),
        i => toCellNum(document.getElementById(`Cell(${(i - i % 9) / 9},${i % 9})`).value)
    ).join('');
}

function updateURLwithCode(code = null) {
    if (code) {
        window.history.pushState({ 'code': code }, 'encoded', `/~${code}`);
    } else {
        window.history.pushState({ 'code': null }, 'base', `/`);
    }
}

async function encode_grid() {
    string = getStringifiedGrid()
    let code = null
    if (Array.from(new Set(string)).join('') != '0') {
        const response = await fetch(`/encode?numbers=${string}`);
        code = await response.text();
    }
    updateURLwithCode(code);
}

function clearGrid() {
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            document.getElementById(`Cell(${i},${j})`).value = "";
        }
    }
    updateURLwithCode(null);
}

function fillGrid(grid) {
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            cell = document.getElementById(`Cell(${i},${j})`);
            cell.value = fromCellValue(grid[i][j]);
        }
    };
    encode_grid();
}


// Screen holding

function playAnimation() {
    a = document.getElementById("animated-svg");
    b = a.contentDocument;
    c = b.getElementById("e6flsqoxhzzs1");
    c.dispatchEvent(new Event("click"));
}

function holdScreen() {
    setStyles(document.getElementById("foreground"), {
        "opacity": 1.0,
        "pointer-events": "auto"
    })
    document.getElementById("content").style["filter"] = "blur(3px) grayscale(35%)"
}

function unHoldScreen() {
    setStyles(document.getElementById("foreground"), {
        "opacity": 0.0,
        "pointer-events": "none"
    })
    document.getElementById("content").style["filter"] = "none"
}


// Service calling

function longCall(f) {
    return async () => {
        holdScreen();
        hideNotification();
        await f();
        unHoldScreen()
    }
}

const getSolverHealth = longCall(async () => {
    const response = await fetch('/solver-health');
    const text = await response.text();

    if (text != 'OK') {
        notify('Error: Solver server is down.');
    };
})

const solve = longCall(async () => {
    const response = await fetch('/solve', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ grid: getGrid() })
    });
    const content = await response.json();

    switch (content["status"]) {
        case "ok":
            fillGrid(content["grid"]);
            break;
        case "error":
            notify(`Error: ${content["error"]}`);
            break;
        default:
            notify("Something went wrong")
    };
})


// Grid cells value input

const cellSetKeys = new Set(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
const cellClearKeys = new Set(["Backspace", " ", "Delete"])
const previousCellValues = {}

document.onkeydown = (e) => {
    const elem = document.activeElement;
    if (elem.className == "grid__input") {
        if (cellSetKeys.has(e.key)) {
            elem.value = e.key;
        } else if (cellClearKeys.has(e.key)) {
            elem.value = "";
        } else {
            return;
        };
        previousCellValues[elem.id] = elem.value;
        encode_grid();
    }
}

const resetPreviousValue = function (elem) {
    elem.value = previousCellValues[elem.id] || "";
};


// Content resizing

function rescale_content() {

    const content = document.getElementById("content");

    const scale = Math.min(window.innerWidth / CONTENT_WIDTH, window.innerHeight / CONTENT_HEIGHT, 1);

    setStyles(content, {
        "transform": `scale(${scale})`,
        "transform-origin": "top left"
    });

    if (scale == 1) {
        content.style.removeProperty("width");
        setStyles(content, {
            "left": 0
        });
    } else {
        setStyles(content, {
            "width": CONTENT_WIDTH + "px",
            "left": Math.max((window.innerWidth - CONTENT_WIDTH * scale) / 2, 0) + "px"
        });
    };

}

window.addEventListener("resize", rescale_content);


// HTML Initalization

window.onload = function () {

    getSolverHealth();

    let gridHtml = "";
    for (let i = 0; i < 9; i++) {
        gridHtml += `<ul class="grid__row">`
        for (let j = 0; j < 9; j++) {
            gridHtml += `
                <li class="grid__item">
                <input type="text" id="Cell(${i},${j})" class="grid__input" inputmode="numeric" oninput="resetPreviousValue(this);">
                </li>
            `
        }
        gridHtml += `</ul>`
    };
    document.getElementById("grid").innerHTML = gridHtml;
    rescale_content();

    if (initialGrid) {
        fillGrid(initialGrid);
    };

    setStyles(document.getElementById("initial-foreground"), {
        "opacity": 0.0,
        "pointer-events": "none"
    })
}


// Test utils

function test() {
    fillGrid(
        [
            [8, null, null, null, null, null, null, null, null],
            [null, null, 3, 6, null, null, null, null, null],
            [null, 7, null, null, 9, null, 2, null, null],
            [null, 5, null, null, null, 7, null, null, null],
            [null, null, null, null, 4, 5, 7, null, null],
            [null, null, null, 1, null, null, null, 3, null],
            [null, null, 1, null, null, null, null, 6, 8],
            [null, null, 8, 5, null, null, null, 1, null],
            [null, 9, null, null, null, null, 4, null, null]
        ]
    )
};
