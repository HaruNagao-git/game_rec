function showModal(src) {
    const modalImage = document.getElementById('modalImage');
    modalImage.src = src;
    const modal = new bootstrap.Modal(document.getElementById('screenshotModal'));
    modal.show();
}
