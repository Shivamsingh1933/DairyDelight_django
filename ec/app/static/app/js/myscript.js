 

 $('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    console.log("pid =", id)
    $.ajax({
        type: "GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success: function(data){
            console.log("data = ",data);
            eml.innerText = data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        }  
    })
 })

 $('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    console.log("pid =", id)
    $.ajax({
        type: "GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success: function(data){
            console.log("data = ",data);
            eml.innerText = data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        }  
    })
 })


 $('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this
    console.log("pid =", id)
    $.ajax({
        type: "GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        success: function(data){
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }  
    })
})

$('.plus-wishlist').click(function() {
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/pluswishlist",
        data: {
            prod_id: id
        },
        success: function(data) {
            if (data.message === "Wishlist Added Successfully") {
                window.location.href = `/product-detail/${id}`;
            }
        },
        error: function(xhr) {
            if (xhr.status === 401) { // Unauthorized
                alert("Your session has expired. Please log in again.");
                window.location.href = "/login/";
            }
        }
    });
});

$('.minus-wishlist').click(function() {
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/minuswishlist",
        data: {
            prod_id: id
        },
        success: function(data) {
            if (data.message === "Wishlist removed Successfully") {
                window.location.href = `/product-detail/${id}`;
            }
        },
        error: function(xhr) {
            if (xhr.status === 401) { // Unauthorized
                alert("Your session has expired. Please log in again.");
                window.location.href = "/login/";
            }
        }
    });
});
