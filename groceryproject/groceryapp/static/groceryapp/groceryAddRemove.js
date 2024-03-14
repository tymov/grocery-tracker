function incrementQuantity(itemId) {
    fetch("/increment_quantity/" + itemId + "/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}", // Replace {{ csrf_token }} with your actual CSRF token
            },
            body: JSON.stringify({}),
        })
        .then((response) => response.json())
        .then((data) => {
            var quantityElement = document.getElementById("quantity_" + itemId);
            var priceElement = document.getElementById("price_" + itemId);
            quantityElement.innerHTML = data.quantity;
            priceElement.innerHTML =
                (data.quantity * data.price).toFixed(2) + "€";
        })
        .catch((error) => console.error("Error:", error));
}

function decrementQuantity(itemId) {
    fetch("/decrement_quantity/" + itemId + "/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}", // Replace {{ csrf_token }} with your actual CSRF token
            },
            body: JSON.stringify({}),
        })
        .then((response) => response.json())
        .then((data) => {
            var quantityElement = document.getElementById("quantity_" + itemId);
            var priceElement = document.getElementById("price_" + itemId);
            quantityElement.innerHTML = data.quantity;
            priceElement.innerHTML =
                (data.quantity * data.price).toFixed(2) + "€";
        })
        .catch((error) => console.error("Error:", error));
}