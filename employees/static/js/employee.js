const current_url = window.location.pathname;
const host = window.location.origin;

let jobTitleCurrentPage = 1;
let bossCurrentPage = 1;

const form = document.getElementById('employee_form')

const employee_photo_url = document.getElementById('employee_photo_url');
const employee_first_name = document.getElementById('employee_first_name');
const employee_middle_name = document.getElementById('employee_middle_name');
const employee_last_name = document.getElementById('employee_last_name');
const employee_job_title = document.getElementById('employee_job_title');
const employee_date_of_receipt = document.getElementById('employee_date_of_receipt');
const employee_wage = document.getElementById('employee_wage');
const employee_boss = document.getElementById('employee_boss');

const loadEmployee = () => {
    const is_create = current_url.match(/\*\/\d\//) === null;

    if (is_create) {
        return;
    }

    return fetch(`${host}/api${current_url}`)
        .then(response => response.json())
        .then(data => {
            const {job_title, boss} = data;

            employee_first_name.value = data.first_name;
            employee_middle_name.value = data.middle_name;
            employee_last_name.value = data.last_name;
            employee_date_of_receipt.value = data.date_of_receipt;
            employee_wage.value = data.wage;

            const option_job_title = document.createElement('option');
            option_job_title.value = job_title.id;
            option_job_title.innerHTML = job_title.title;
            employee_job_title.appendChild(option_job_title);

            if (data.photo !== null) {
                employee_photo_url.classList.remove('d-block')
                employee_photo_url.src = data.photo;
                employee_photo_url.style.border = '1px solid black';
            }

            if (boss !== null) {
                const option_boss = document.createElement('option');
                option_boss.value = boss.id;
                option_boss.innerHTML = `${boss.last_name} ${boss.first_name} ${boss.middle_name}`;
                option_boss.selected = 'selected';
                employee_boss.appendChild(option_boss);
            }
        });
}

document.getElementById('btn-delete')
    .addEventListener('click', event => {
        return fetch(`${host}/api${current_url}`, {
            method: 'DELETE',
            headers: {
                "X-CSRFToken": Cookies.get('csrftoken'),
            },
        }).then(response => {
            if (response.status === 204) {
                alertify.alert('Данные успешно удалены.')
                    .set({
                        onclose: () => {
                            window.location.replace(`${host}/employee/`);
                        },
                    });
            } else {
                alertify.error('Произошла ошибка, попробуйте позже.');
            }
        })
    });

const btn_load_job_title = document.getElementById('btn-load-job-title');
btn_load_job_title.addEventListener('click', event => {
    return fetch(`http://127.0.0.1:8000/api/jobtitle/?page=${jobTitleCurrentPage}`)
        .then(response => response.json())
        .then(data => {
            data.results.forEach(item => {
                if (employee_job_title.length >= 1 && item.id === employee_job_title[0].value) {
                    return;
                }

                const option = document.createElement('option');
                option.value = item.id;
                option.innerHTML = item.title;

                employee_job_title.appendChild(option);
            });

            if (data.next !== null) {
                jobTitleCurrentPage += 1;
            } else {
                btn_load_job_title.remove();
            }
        });
});

const btn_load_boss = document.getElementById('btn-load-boss');
btn_load_boss.addEventListener('click', event => {
    return fetch(`http://127.0.0.1:8000/api/employee/?page=${bossCurrentPage}`)
        .then(response => response.json())
        .then(data => {
            data.results.forEach(item => {
                if (employee_boss.length >= 2 && item.id == employee_boss[1].value) {
                    return;
                }

                const option = document.createElement('option');
                option.value = item.id;
                option.innerHTML = `${item.last_name} ${item.first_name} ${item.middle_name}`;

                employee_boss.appendChild(option);
            });

            if (data.next !== null) {
                bossCurrentPage += 1;
            } else {
                btn_load_boss.remove();
            }
        });
});

const btn_save = document.getElementById("btn-save");
btn_save.addEventListener('click', event => {
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    let url;
    let method;
    let status;

    const is_create = current_url.match(/\*\/\d\//) === null;

    if (is_create) {
        url = `${host}/api/employee/`;
        method = 'POST';
        status = 201;
    } else {
        url = `${host}/api${current_url}`;
        method = 'PUT';
        status = 200;
    }

    return fetch(url, {
        method: method,
        body: new FormData(form),
        headers: {
            "X-CSRFToken": Cookies.get('csrftoken'),
        },
    }).then(response => {
        if (response.status === status) {
            alertify.success('Данные успешно сохранены.');
        } else {
            alertify.error('Произошла ошибка, попробуйте позже.');
        }
    });
});

window.onload = loadEmployee();