function search(button) {
    let array = button.parentNode.childNodes
    for (var i = 0; i < array.length; i++) {
        let child = array[i]
        if (child.value) {
            const request = new XMLHttpRequest();

            const url = "/search" + "?" + "what=" + child.id + "&value=" + child.value;
            request.open('GET', url);
            request.setRequestHeader('Content-Type', 'application/x-www-form-url');
            request.addEventListener("readystatechange", () => {
                if (request.readyState === 4 && request.status === 200) {
                    let parent_forms = document.getElementById('main_info')

                    var loan_app_json = JSON.parse(decodeURIComponent(request.response))
                    let array_main_info_childs = parent_forms.childNodes
                    let for_not_delete_1_form = 0

                    let phone_number = loan_app_json.client_fk
                    let product = loan_app_json.product
                    let solution = loan_app_json.solution
                    let date = loan_app_json.date_application
                    let id = loan_app_json.id
                    let comment = loan_app_json.text_comment

                    for (var i = 0; i < array_main_info_childs.length; i++) {

                        let child = array_main_info_childs[i]

                        if (child.nodeName === 'FORM' && for_not_delete_1_form === 0) {
                            console.log(child.childNodes[3])
                            for_not_delete_1_form++
                        } else if (child.nodeName === 'FORM') {
                            document.getElementById('main_info').removeChild(child)
                        }
                    }

                    document.getElementById('id_phone_number').value = phone_number
                    document.getElementById('id').value = id
                    document.getElementById('id_product').value = product
                    document.getElementById('id_solution').value = solution
                    document.getElementById('id_date_application').value = date
                    document.getElementById('id_comment').value = comment

                    // parent_forms.insertAdjacentHTML()

                }
            });
            request.send();

        }

    }
}

function check_status(field_set, id) {
    const request = new XMLHttpRequest();

    const url = "/check_status" + "?" + "loan_application=" + field_set.id + "&user=" + id;
    request.open('GET', url);
    request.setRequestHeader('Content-Type', 'application/x-www-form-url');

    request.addEventListener("readystatechange", () => {
        if (request.readyState === 4 && request.status === 200) {
            var access_to_forms = request.response
            if (access_to_forms === 'False') {
                field_set.setAttribute('disabled', 'disabled');
            } else if (access_to_forms === 'True') {
                field_set.removeAttribute('disabled');
            }


        }
    });
    request.send();
}

function set_status(field_set, id) {
    const request = new XMLHttpRequest();
    const url = "/set_status" + "?" + "loan_application=" + field_set.id + "&user=" + id;
    request.open('GET', url);
    request.setRequestHeader('Content-Type', 'application/x-www-form-url');

    request.addEventListener("readystatechange", () => {
        if (request.readyState === 4 && request.status === 200) {
        }
    });
    request.send();
}

function delete_status(field_set) {
    let nodes = field_set.target.parentElement.parentElement.childNodes
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].id === 'id') {
            const request = new XMLHttpRequest();
            const url = "/delete_status" + "?" + "loan_application=" + nodes[i].value;
            request.open('GET', url);
            request.setRequestHeader('Content-Type', 'application/x-www-form-url');

            request.addEventListener("readystatechange", () => {
                if (request.readyState === 4 && request.status === 200) {
                }
            });
            request.send();

            break
        }
    }
}

window.addEventListener("focusout", delete_status);
