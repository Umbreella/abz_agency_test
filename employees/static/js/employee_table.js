const ul_main = document.querySelector('.list_main');
const pagination = document.querySelector('.pagination');
const search_text = document.getElementById('search');
const order_select = document.getElementById('orderBy');

const refreshData = (page) => {
    ul_main.innerHTML = '';
    loadData(null, ul_main, null, page);
}

document.querySelector('.search_btn')
    .addEventListener('click', event => {
        refreshData(1);
    }, false);

const loadData = (base_url, insert_element, boss_id, page) => {
    let url = '';

    if (base_url === null) {
        url += `http://127.0.0.1:8000/api/employee/?`;
        url += `&search=${search_text.value}`;
        url += `&page=${page}`;
        url += `&ordering=${order_select.value}`;

        if (boss_id !== null) {
            url += `&boss=${boss_id}`;
        } else {
            url += `&boss_null=1`;
        }
    } else {
        url += base_url;
    }

    return fetch(url)
        .then(response => response.json())
        .then(data => {
            data.results.forEach(item => {
                const li_item = document.createElement('li');
                li_item.innerHTML = `
                    <div class="container">
                        <div class="row">
                            <div class="col-1" style="border: 1px solid black;">
                                ${
                    item.photo !== null ?
                        `<img src="${item.photo}" width="100%">` :
                        `<div></div>`
                }
                            </div>
                            <div class="col-3">
                                ${item.first_name} ${item.middle_name} ${item.last_name}
                            </div>
                            <div class="col-2">
                                ${item.job_title.title}
                            </div>
                            <div class="col-2">
                                ${item.date_of_receipt}
                            </div>
                            <div class="col-2">
                                ${item.wage}
                            </div>
                            <div class="col-2">
                                <a href="http://127.0.0.1:8000/employee/${item.id}/" class="btn btn-primary">
                                    <i class="fa fa-pencil"></i>
                                </a>
                                <div class="btn btn-info">
                                    <i class="fa fa-folder"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                `;

                const drag_and_drop_container = li_item.querySelector('.container');
                drag_and_drop_container.draggable = true;

                drag_and_drop_container.ondragover = event => {
                    event.preventDefault();
                }

                drag_and_drop_container.ondragstart = event => {
                    event.dataTransfer.setData('id', item.id);
                    event.dataTransfer.setData('boss', item.boss?.id);
                }

                drag_and_drop_container.ondrop = event => {
                    const child_id = event.dataTransfer.getData('id');
                    const boss_id = event.dataTransfer.getData('boss');

                    if (item.id == child_id) {
                        return null;
                    }

                    if (boss_id !== undefined && item.id == boss_id) {
                        return null;
                    }

                    return fetch(`http://127.0.0.1:8000/api/employee/${child_id}/`, {
                        method: 'PATCH',
                        body: JSON.stringify({
                            'boss_id': item.id,
                        }),
                        headers: {
                            "X-CSRFToken": Cookies.get('csrftoken'),
                            "Content-type": "application/json",
                        },
                    }).then(response => {
                        if (response.status === 200) {
                            alertify.success('Данные успешно сохранены.' +
                                ' Обновите странице.');
                        } else {
                            alertify.error('Произошла ошибка, попробуйте позже.');
                        }
                    });
                }

                const btn_info = li_item.querySelector('.btn-info');

                const recursive = (event) => {
                    btn_info.removeEventListener('click', recursive, false);
                    btn_info.remove();

                    const ul_item = document.createElement('ul');
                    li_item.insertAdjacentElement('beforeend', ul_item);

                    loadData(null, ul_item, item.id, 1);
                }

                btn_info.addEventListener('click', recursive, false);

                insert_element.insertAdjacentElement('beforeend', li_item);
            });

            if (data.next !== null) {
                const loadMore = document.createElement('div');
                loadMore.classList.add('d-flex', 'justify-content-center', 'm-5');
                loadMore.innerHTML = `
                        <button type="button" class="btn btn-primary">Загрузить еще</button>
                    `;

                loadMore.addEventListener('click', event => {
                    loadMore.remove();
                    loadData(data.next, insert_element, null, null);
                })

                insert_element.insertAdjacentElement('beforeend', loadMore);
            }
        });
}


window.onload = loadData(null, ul_main, null, 1);
