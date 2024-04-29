const custId = document.querySelector("#custid");
const fetchOrderBtn = document.querySelector(".fetch-orders-btn");
const orderTable = document.querySelector(".order-table");
const detailTable = document.querySelector(".details-table");

const detailsTableHeadRow = `<tr>
<th>Product</th>
<th>Quantity</th>
<th>Sales</th>
<th>Discount</th>
<th>Shipping Cost</th>
<th>Ship Mode</th>
</tr>`;

let prevOrderId = "";

function fetchDetails(e) {
  let orderId = e.target.id;
  if (prevOrderId == orderId) {
    return;
  }
  console.log("Fetching details...");
  fetch(`/fetch-details?orderid=${orderId}`)
    .then((res) => res.json())
    .then((res) => {
      let details = res["details"];
      console.log(details);
      detailTable.innerHTML = detailsTableHeadRow;
      details.forEach((orderDetail) => {
        detailTable.innerHTML += getDetailRow(orderDetail);
      });
      detailTable.classList.add("active");
      prevOrderId = orderId;
    });
}

function getDetailRow(d) {
  return `<tr>
    <td>${d["prodname"]}</td>
    <td>${d["quantity"]}</td>
    <td>${d["sale"]}</td>
    <td>${d["discount"]}</td>
    <td>${d["shippingcost"]}</td>
    <td>${d["shipmode"]}</td>
    </tr>`;
}

function setListeners() {
  let detailBtns = document.querySelectorAll(".details-btn");
  detailBtns.forEach((btn) => {
    btn.addEventListener("click", fetchDetails);
  });
}

function fetchOrders() {
  if (orderTable.classList.contains("active")) {
    return;
  }
  console.log("Fetching orders...");
  fetch(`/fetch-orders?custid=${custId.innerText}`)
    .then((res) => res.json())
    .then((res) => {
      let orders = res["orders"];
      console.log(orders);
      orders.forEach((order) => {
        orderTable.innerHTML += getOrderRow(order);
      });
      orderTable.classList.add("active");
      setListeners();
    });
}

function getOrderRow(order) {
  return `<tr><td>${order["orderid"]}</td><td>${
    order["custname"]
  }</td><td>${getFetchProdBtn(order["orderid"])}</td>`;
}

function getFetchProdBtn(orderid) {
  return `<button class='btn details-btn' id=${orderid}>Details</button>`;
}

fetchOrderBtn.addEventListener("click", fetchOrders);
