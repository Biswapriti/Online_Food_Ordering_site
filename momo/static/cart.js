// Cart functionality
document.addEventListener('DOMContentLoaded', () => {
    const cartList = document.querySelector('.cart-list');
    if (!cartList) return; // Not on cart page

    // Handle quantity changes
    cartList.addEventListener('click', (e) => {
        const item = e.target.closest('.cart-item');
        if (!item) return;
        
        // Handle quantity buttons
        if (e.target.matches('.quantity-btn')) {
            const input = item.querySelector('.quantity-input');
            const currentQty = parseInt(input.value);
            const isPlus = e.target.classList.contains('plus');
            
            const newQty = isPlus ? currentQty + 1 : currentQty - 1;
            if (newQty > 0 && newQty <= 99) {
                input.value = newQty;
                updateItemQuantity(item.dataset.id, newQty);
            }
        }
        
        // Handle remove button
        if (e.target.matches('.remove-item')) {
            removeItem(item.dataset.id);
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
            setTimeout(() => {
                item.remove();
                updateEmptyState();
            }, 250);
        }
    });

    // Handle direct quantity input
    cartList.addEventListener('change', (e) => {
        if (e.target.matches('.quantity-input')) {
            const item = e.target.closest('.cart-item');
            const newQty = parseInt(e.target.value);
            if (newQty > 0 && newQty <= 99) {
                updateItemQuantity(item.dataset.id, newQty);
            } else {
                e.target.value = 1;
                updateItemQuantity(item.dataset.id, 1);
            }
        }
    });

    // Update cart on server
    async function updateItemQuantity(itemId, quantity) {
        try {
            // Update local cart first
            const cart = JSON.parse(localStorage.getItem('cart') || '[]');
            const item = cart.find(i => i.id === itemId);
            if (item) {
                item.quantity = quantity;
                localStorage.setItem('cart', JSON.stringify(cart));
            }

            // Then sync with server
            const response = await fetch('/cart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(cart)
            });

            if (!response.ok) throw new Error('Failed to update cart');
            
            // Update UI
            updateCartTotal();
            updateItemTotal(itemId, item.price, quantity);
            
        } catch (err) {
            console.error('Failed to update cart:', err);
        }
    }

    // Remove item from cart
    async function removeItem(itemId) {
        try {
            const cart = JSON.parse(localStorage.getItem('cart') || '[]');
            const newCart = cart.filter(i => i.id !== itemId);
            localStorage.setItem('cart', JSON.stringify(newCart));

            // Sync with server
            const response = await fetch('/cart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newCart)
            });

            if (!response.ok) throw new Error('Failed to update cart');
            
            // Update UI
            updateCartTotal();
            
        } catch (err) {
            console.error('Failed to remove item:', err);
        }
    }

    // Update item's total price display
    function updateItemTotal(itemId, price, quantity) {
        const item = document.querySelector(`.cart-item[data-id="${itemId}"]`);
        if (item) {
            const totalEl = item.querySelector('.item-total');
            if (totalEl) {
                totalEl.textContent = `$${(price * quantity).toFixed(2)}`;
            }
        }
    }

    // Update cart total
    function updateCartTotal() {
        const cart = JSON.parse(localStorage.getItem('cart') || '[]');
        const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        
        const totalEl = document.querySelector('.cart-total strong');
        if (totalEl) {
            totalEl.textContent = `$${total.toFixed(2)}`;
        }
    }

    // Show empty state if cart is empty
    function updateEmptyState() {
        const cart = JSON.parse(localStorage.getItem('cart') || '[]');
        const container = document.querySelector('.cart-container');
        const emptyState = document.querySelector('.empty-cart');
        
        if (cart.length === 0) {
            if (container) container.style.display = 'none';
            if (emptyState) emptyState.style.display = 'block';
        }
    }

    // initialize UI on load
    updateCartTotal();
    updateEmptyState();
});