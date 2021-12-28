// CSS utils

function styleValueToNumber(string) {
    return parseFloat(string.replace(/[^\d]+/g, ''));
}

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

const $ = (str) => document.getElementById(str);

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

const grid_history = {
    _hist: [],
    push: function (grid) {
        if (this._hist.length == 0 || !equalGrid(grid, this._hist[this._hist.length - 1])) {
            this._hist.push(grid);
            document.getElementById("btn-revert").disabled = (this._hist.length < 2);
        }
    },
    pop: function () {
        if (this._hist.length >= 2) {
            this._hist.pop();
            if (this._hist.length < 2) {
                document.getElementById("btn-revert").disabled = true;
            };
            return this._hist.pop();
        };
        return null;
    },
    empty: function () {
        this._hist = [];
    }
}

function getEmptyGrid() {
    return Array.from(
        Array(9).keys(),
        i => Array.from(
            Array(9).keys(),
            j => null
        )
    );
}

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

function equalGrid(grid_1, grid_2) {
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            if (grid_1[i][j] != grid_2[i][j]) return false;
        }
    };
    return true;
}

function updateURLwithCode(code = null) {
    if (code) {
        window.history.pushState({ 'code': code }, '', `/~${code}`);
    } else {
        window.history.pushState({ 'code': null }, '', `/`);
    }
}

async function encode_grid() {
    grid_history.push(getGrid());
    string = getStringifiedGrid()
    let code = null
    if (Array.from(new Set(string)).join('') != '0') {
        const response = await fetch(`/encode?numbers=${string}`);
        code = await response.text();
    }
    updateURLwithCode(code);
}

function revertGrid() {
    let grid = grid_history.pop();
    if (grid != null) {
        fillGrid(grid);
    };
}

function clearGrid() {
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            document.getElementById(`Cell(${i},${j})`).value = "";
        }
    }
    encode_grid();
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

async function validateCell(cell) {
    const is_valid = await is_valid_grid();
    if (is_valid === false) {
        setStyles(cell, { "color": "red", "font-weight": 600 })
    } else {
        Array.from(document.getElementsByClassName("grid__input")).forEach(element => {
            setStyles(element, { "color": "black", "font-weight": 400 })
        });
    }
}


// Screen holding

//function playAnimation() {
//    a = document.getElementById("animated-svg");
//    b = a.contentDocument;
//    c = b.getElementById("e6flsqoxhzzs1");
//    c.dispatchEvent(new Event("click"));
//}

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

const generate = longCall(async () => {
    const response = await fetch('/get_task', {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }
    });
    const content = await response.json();

    switch (content["status"]) {
        case "ok":
            grid_history.empty();
            fillGrid(content["grid"]);
            break;
        case "error":
            notify(`Error: ${content["error"]}`);
            break;
        default:
            notify("Something went wrong")
    };
})

const is_valid_grid = async () => {
    const response = await fetch('/validate?' + new URLSearchParams({ "numbers": getStringifiedGrid() }));
    const content = await response.json();
    return content["is_valid"];
};


// Generate menu logic

function showGenMenu() {

    btn_menu_rect = $("gen-menu").getBoundingClientRect();
    btn_generate_rect = $("btn-generate").getBoundingClientRect();

    setStyles($("gen-menu-container"), {
        visibility: "visible",
        top: btn_generate_rect.top - btn_menu_rect.height + "px",
        left: btn_generate_rect.left + "px",
        width: btn_generate_rect.width + "px",
        height: btn_menu_rect.height + "px"
    });

    $("gen-menu").classList.add("dropdown-menu--unfolded");
    $("btn-generate").classList.add("btn-main-menu--toggled");

}

function hideGenMenu() {

    setStyles($("gen-menu-container"), {
        visibility: "hidden"
    });

    $("gen-menu").classList.remove("dropdown-menu--unfolded");
    $("btn-generate").classList.remove("btn-main-menu--toggled");

}

window.addEventListener('click', function (e) {
    if ($("gen-menu-container").style.visibility == "visible") {
        hideGenMenu();
    } else if (e.target.id == "btn-generate") {
        showGenMenu();
    };
});

window.addEventListener("resize", function () {
    hideGenMenu();
});

// Grid cells value input

const cellSetKeys = new Set(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
const cellClearKeys = new Set(["Backspace", " ", "Delete"])
const previousCellValues = {}

document.onkeydown = (e) => {
    const elem = document.activeElement;
    if (elem.className == "grid__input") {
        if (cellSetKeys.has(e.key)) {
            elem.value = e.key;
            // validateCell(elem);
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

    fillGrid(initialGrid ? initialGrid : getEmptyGrid());

    setStyles(document.getElementById("initial-foreground"), {
        "opacity": 0.0,
        "pointer-events": "none"
    })
}
