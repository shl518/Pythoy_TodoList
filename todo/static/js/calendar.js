const date = new Date();

const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
];

const months_dic = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
};

const tag_choices = {
    0: "运动",
    1: "学习",
    2: "饮食",
    3: "工作",
    4: "休闲",
    5: "生活",
    6: "其他",
}

const status = {
    0: "未开始",
    1: "进行中",
    2: "已完成",
    3: "已过期",
}

const importance = {
    0: "不紧急任务",
    1: "普通任务",
    2: "优先任务",
    3: "突发紧急任务",
}

const daily = {
    True: "是",
    False: "否",
}

const Message = (id) => {
    const list = document.getElementById("chose-date").innerHTML.split("   ") + "," +
        document.getElementById(id).innerHTML.split(",").toString().split(",");
    return list.split(",");
}

const show = (json, target) => {
    if (json.length > 0) {
        let divs = "";
        for (let i = 0; i < json.length; i++) {
            divs += `<div class="issue-column">`;
            divs += `<div class="issue-title">` + 'Title : ' + json[i].title + `</div>`;
            divs += `<div class="issue-tag">` + 'Tag : ' + tag_choices[json[i].tag] + `</div>`;
            divs += `<div class="issue-start">` + 'Start Time : ' + json[i].expiration_date.split("T")[1].slice(0, 5) + `</div>`;
            divs += `<div class="issue-duration">` + 'Duration : ' + json[i].predict_hour + 'h' + json[i].predict_minute + 'min' + '</div>';
            divs += `<div class="issue-status">` + 'Status : ' + status[json[i].status] + `</div>`
            divs += `<div class="issue-importance">` + 'Importance : ' + importance[json[i].status] + `</div>`;
            divs += `<div class="issue-daily">` + 'Daily : ' + json[i].isDaily + `</div>`;
            divs += `</div>`;
        }
        target.innerHTML = divs;
    } else {
        target.innerHTML = `<div class="issue-nothing">` + 'You have no mission this day!' + `</div>`;
    }
}

const today = () => {
    const xhr = new XMLHttpRequest();
    const dt = new Date();
    const year = dt.getFullYear(), month = dt.getMonth() + 1, date = dt.getDate();
    const phrase = 'month=' + month + '&year=' + year + '&date=' + date;
    xhr.open('GET', 'http://127.0.0.1:8000/calendar/today?' + phrase);
    xhr.send();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status >= 200 && xhr.status < 300) {
                const json = JSON.parse(xhr.response);
                const target = document.getElementById("matters");
                show(json, target);
            }
        }
    }
}

const renderCalendar = () => {
    date.setDate(1);

    const monthDays = document.querySelector(".days");

    const lastDay = new Date(
        date.getFullYear(),
        date.getMonth() + 1,
        0
    ).getDate();

    const prevLastDay = new Date(
        date.getFullYear(),
        date.getMonth(),
        0
    ).getDate();

    const firstDayIndex = date.getDay();

    const lastDayIndex = new Date(
        date.getFullYear(),
        date.getMonth() + 1,
        0
    ).getDay();

    const nextDays = 7 - lastDayIndex - 1;

    document.querySelector(".date h1").innerHTML = months[date.getMonth()] + "   " + date.getFullYear().toString();
    document.querySelector(".date p").innerHTML = new Date().toDateString();

    let days = "";

    for (let x = firstDayIndex; x > 0; x--) {
        days += `<div class="prev-date">${prevLastDay - x + 1}</div>`;
    }

    for (let i = 1; i <= lastDay; i++) {
        if (
            i === new Date().getDate() &&
            date.getMonth() === new Date().getMonth()
        ) {
            days += `<div class="today" id=${i}>${i}</div>`;
        } else {
            days += `<div id=${i}>${i}</div>`;
        }
    }

    for (let j = 1; j <= nextDays; j++) {
        days += `<div class="next-date">${j}</div>`;
        monthDays.innerHTML = days;
    }

    for (let i = 1; i <= lastDay; i++) {
        let block = document.getElementById(i.toString())
        block.onclick = function () {
            /* 1.创建对象 2.初始化请求方法并设置url 3.发送 4.事件绑定 */
            const xhr = new XMLHttpRequest();
            const phrase = 'month=' + Message(i)[0] + '&year=' + Message(i)[1] + '&date=' + Message(i)[2];
            const target = document.getElementById("matters");
            const the_day = document.getElementById("mission");
            the_day.innerText = 'Missions of ' + Message(i)[1] + '.' + months_dic[Message(i)[0]] + '.' + Message(i)[2];
            xhr.open('GET', 'http://127.0.0.1:8000/calendar/whichdate?' + phrase);
            xhr.send();
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4) {
                    if (xhr.status >= 200 && xhr.status < 300) {
                        const json = JSON.parse(xhr.response);
                        show(json, target);
                    }
                }
            }
        }
    }

    today();
};

document.querySelector(".prev").addEventListener("click", () => {
    date.setMonth(date.getMonth() - 1);
    renderCalendar();
});

document.querySelector(".next").addEventListener("click", () => {
    date.setMonth(date.getMonth() + 1);
    renderCalendar();
});

renderCalendar();