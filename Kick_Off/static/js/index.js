// Function for drop menu in the nav bar

const toggle_slider = () => {
    const toggle_slider = document.getElementById("toggle_slider");
    const slider = document.getElementById("slider");
    if (slider.style.top === "-100dvh" || slider.style.top === "") {
        slider.style.top = "4rem";
        toggle_slider.style.color = "rgb(223, 62, 62)";
        toggle_slider.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="23" height="23" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16"><path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z" /></svg >'
    } else {
        slider.style.top = "-100dvh";
        toggle_slider.style.color = "black";
        toggle_slider.innerHTML = '<svg xmlns = "http://www.w3.org/2000/svg" width = "25" height = "25" fill = "currentColor" class="bi bi-list" viewBox = "0 0 16 16"><path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5"/></svg >'
    }
}

// Function to perform bookmark without loading the html page

const bookmark_request = (bookmark_data) => {
    fetch('/save_this_event/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(bookmark_data)
    }).then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error status: ${response.status}`);
        }
        return response.json();
    })
        .then(data => {
            if (data.login_required) {
                window.location.href = '/login/'
            }
            else if (data.bookmarked) {
                document.getElementById('bookmark_icon').innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bookmark-check" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M10.854 5.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 7.793l2.646-2.647a.5.5 0 0 1 .708 0"/><path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1z"/></svg>'
            }
            else {
                document.getElementById('bookmark_icon').innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bookmark" viewBox="0 0 16 16"><path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1z"/></svg>'
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const ticket_count = (ticket_count_data) => {
    const current_ticket_count = parseInt(document.getElementById('ticket_count').innerHTML);
    if (ticket_count_data.status === "POSITIVE") {
        const updated_ticket_count = current_ticket_count + 1
        if (updated_ticket_count <= ticket_count_data.total_tickets) {
            document.getElementById('ticket_count').innerHTML = `${updated_ticket_count}`
            const ammount_payable = updated_ticket_count * ticket_count_data.ticket_price
            document.getElementById('ticket_price').innerHTML = `${ammount_payable}`
        }
    } else {
        const updated_ticket_count = current_ticket_count - 1
        if (!updated_ticket_count <= 0) {
            document.getElementById('ticket_count').innerHTML = `${updated_ticket_count}`
            const ammount_payable = updated_ticket_count * ticket_count_data.ticket_price
            document.getElementById('ticket_price').innerHTML = `${ammount_payable}`
        }
    }
}

const make_payment = (event_id) => {
    if (confirm("Are you sure you want to purchase this ticket?")) {
        const ticket_details = {
            'event_number_of_tickets': parseInt(document.getElementById('ticket_count').innerHTML),
            'event_ticket_price': parseInt(document.getElementById('ticket_price').innerHTML)

        }
        fetch(`/book_now/${event_id}/book_tickets/make_payment/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(ticket_details)
        }).then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error status: ${response.status}`);
            }
            return response.json();
        })
            .then(data => {
                if (data.login_required) {
                    window.location.href = '/login/'
                }
                else if (data.payment_status) {
                    document.getElementById('payment_form').reset()
                    window.location.href = '/tickets_booked/'
                }
                else {
                    alert("Payment failed. Please try again")
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    } else {
        alert("Payement cancelled.")
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('payment_form') &&
        document.getElementById('payment_form').reset()

})

const delete_event_alert = () => {
    return confirm('Are you sure you want to delete')
}