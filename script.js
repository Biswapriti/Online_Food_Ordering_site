document.addEventListener('DOMContentLoaded', function () {
	// Mobile nav toggle
	const navToggle = document.getElementById('nav-toggle');
	const siteNav = document.getElementById('site-navigation');
	if (navToggle && siteNav) {
		navToggle.addEventListener('click', () => {
			const expanded = navToggle.getAttribute('aria-expanded') === 'true';
			navToggle.setAttribute('aria-expanded', String(!expanded));
			siteNav.classList.toggle('open');
		});
	}

	// Enhanced menu filtering with multiple categories + cross-page behavior
	const chips = document.querySelectorAll('.chip');
	const items = document.querySelectorAll('.menu-item');
	const menuGrid = document.querySelector('.menu-grid');
	const isMenuPage = window.location.pathname === '/menu' || window.location.pathname.endsWith('/menu');

	if (chips.length === 0) console.warn('No menu filter chips found');
	if (items.length === 0) console.warn('No menu items found to filter');

	// store original chip labels so we can append counts
	chips.forEach(c => {
		c.dataset.label = c.textContent.trim();
	});

	function updateChipCounts() {
		chips.forEach(c => {
			const key = c.dataset.filter;
			let count = 0;
			items.forEach(it => {
				const types = (it.dataset.type || '').split(' ');
				if (key === 'all' || types.includes(key)) count += 1;
			});
			// render label + count
			const label = c.dataset.label || c.textContent.trim();
			c.innerHTML = `<span class="chip-label">${label}</span> <span class="chip-count">(${count})</span>`;
		});
	}

	function filterItems(filterValue) {
		items.forEach(item => {
			const types = (item.dataset.type || '').split(' ');
			const shouldShow = filterValue === 'all' || types.includes(filterValue);
			if (shouldShow) {
				item.style.opacity = '0';
				item.style.display = '';
				requestAnimationFrame(() => {
					item.style.opacity = '1';
					item.style.transform = 'translateY(0)';
				});
			} else {
				item.style.opacity = '0';
				item.style.transform = 'translateY(20px)';
				setTimeout(() => { item.style.display = 'none'; }, 300);
			}
		});
		updateChipCounts();
	}

	// If we're on the homepage (not /menu), clicking a chip should navigate to the full menu page with the filter applied.
	// On the /menu page chips support multi-select: each chip toggles active state and filtering is the OR of selected filters.
	chips.forEach(chip => {
		chip.addEventListener('click', (ev) => {
			ev.preventDefault();
			const filter = (chip.getAttribute('data-filter') || 'all').toLowerCase();

			if (!isMenuPage) {
				// redirect to full menu page with optional query param (single filter)
				const url = filter === 'all' ? '/menu' : `/menu?filter=${encodeURIComponent(filter)}`;
				window.location.href = url;
				return;
			}

			// On /menu: multi-select behavior
			if (filter === 'all') {
				// Clear all other selections and show all
				chips.forEach(c => c.classList.remove('active'));
				chip.classList.add('active');
				filterItems('all');
				const menuSection = document.getElementById('menu');
				if (menuSection) menuSection.scrollIntoView({ behavior: 'smooth' });
				return;
			}

			// Toggle this chip
			chip.classList.toggle('active');
			// If any non-all chip is active, remove 'all'
			const anySelected = Array.from(chips).some(c => c.classList.contains('active') && c.dataset.filter !== 'all');
			if (anySelected) {
				document.querySelectorAll('.chip[data-filter="all"]').forEach(a => a.classList.remove('active'));
			} else {
				// If nothing selected, re-select 'all'
				const allChip = document.querySelector('.chip[data-filter="all"]');
				if (allChip) allChip.classList.add('active');
			}

			// Compute selected filters
			const selectedFilters = Array.from(chips)
				.filter(c => c.classList.contains('active') && c.dataset.filter !== 'all')
				.map(c => c.dataset.filter);

			if (selectedFilters.length === 0) {
				filterItems('all');
			} else {
				// Show items that match ANY of the selected filters (OR)
				items.forEach(item => {
					const types = (item.dataset.type || '').split(' ');
					const matched = selectedFilters.some(f => types.includes(f));
					if (matched) {
						item.style.display = '';
						item.style.opacity = '0';
						requestAnimationFrame(() => { item.style.opacity = '1'; item.style.transform = 'translateY(0)'; });
					} else {
						item.style.opacity = '0';
						item.style.transform = 'translateY(20px)';
						setTimeout(() => { item.style.display = 'none'; }, 250);
					}
				});
				updateChipCounts();
			}

			const menuSection = document.getElementById('menu');
			if (menuSection) menuSection.scrollIntoView({ behavior: 'smooth' });
		});
	});

	// If we're on /menu and a filter query param is present, apply it on load (supports comma-separated filters)
	if (isMenuPage) {
		const params = new URLSearchParams(window.location.search);
		const fparam = (params.get('filter') || '').toLowerCase();
		// Clear any active states first
		chips.forEach(c => c.classList.remove('active'));

		if (!fparam || fparam === 'all') {
			// show all
			const allChip = document.querySelector('.chip[data-filter="all"]');
			if (allChip) allChip.classList.add('active');
			filterItems('all');
		} else {
			const keys = fparam.split(',').map(s => s.trim()).filter(Boolean);
			// mark matching chips active
			keys.forEach(k => {
				const chip = document.querySelector(`.chip[data-filter="${k}"]`);
				if (chip) chip.classList.add('active');
			});

			// Apply OR-filtering based on selected chips
			const selectedFilters = Array.from(chips)
				.filter(c => c.classList.contains('active') && c.dataset.filter !== 'all')
				.map(c => c.dataset.filter);

			if (selectedFilters.length === 0) {
				filterItems('all');
			} else {
				items.forEach(item => {
					const types = (item.dataset.type || '').split(' ');
					const matched = selectedFilters.some(f => types.includes(f));
					if (matched) {
						item.style.display = '';
						item.style.opacity = '0';
						requestAnimationFrame(() => { item.style.opacity = '1'; item.style.transform = 'translateY(0)'; });
					} else {
						item.style.opacity = '0';
						item.style.transform = 'translateY(20px)';
						setTimeout(() => { item.style.display = 'none'; }, 250);
					}
				});
				updateChipCounts();
			}
		}
	} else {
		// not menu page: update counts based on items present (may be subset)
		updateChipCounts();
	}

	// Shopping cart functionality
	const cart = {
		items: JSON.parse(localStorage.getItem('cart') || '[]'),
		
		addItem(id, name, price) {
			const existingItem = this.items.find(item => item.id === id);
			if (existingItem) {
				existingItem.quantity += 1;
			} else {
				this.items.push({ id, name, price, quantity: 1 });
			}
			this.save();
			this.updateUI();
		},
		
		save() {
			localStorage.setItem('cart', JSON.stringify(this.items));
		},
		
		updateUI() {
			// Show a quick feedback animation
			const notification = document.createElement('div');
			notification.className = 'cart-notification';
			notification.textContent = 'Added to cart!';
			document.body.appendChild(notification);
			
			setTimeout(() => {
				notification.remove();
			}, 2000);
		}
	};

	// Add click handlers for cart buttons — add item then redirect to cart page
	document.querySelectorAll('.btn-cart').forEach(button => {
		button.addEventListener('click', async (e) => {
			const item = e.target.closest('.menu-item');
			const name = item.querySelector('h3').textContent;
			const id = e.target.closest('.btn-cart').dataset.id;
			const price = parseFloat(e.target.closest('.btn-cart').dataset.price);

			try {
				await cart.addItem(id, name, price);
			} catch (err) {
				console.error('Failed to add item before redirect:', err);
			}

			// Button click animation
			button.style.transform = 'scale(0.95)';
			setTimeout(() => { button.style.transform = ''; }, 100);

			// Navigate to cart page only when the button requests it (data-redirect="true" or class 'go-cart')
			const shouldRedirect = button.dataset.redirect === 'true' || button.classList.contains('go-cart');
			if (shouldRedirect) window.location.href = '/cart';
		});
	});

	// Simple testimonial rotation
	const slider = document.getElementById('testimonials');
	if (slider) {
		let idx = 0;
		const slides = Array.from(slider.querySelectorAll('.testimonial'));
		if (slides.length > 0) {
			slides.forEach((s, i) => s.style.display = i === 0 ? 'block' : 'none');
			setInterval(() => {
				slides[idx].style.display = 'none';
				idx = (idx + 1) % slides.length;
				slides[idx].style.display = 'block';
			}, 4000);
		}
	}

	// Theme toggle: persist selection and default to dark on homepage
	const themeToggle = document.getElementById('theme-toggle');
	const body = document.body;

	function applyTheme(name){
		if(name === 'dark'){
			body.classList.add('dark-theme');
			if(themeToggle) themeToggle.setAttribute('aria-pressed','true');
			if(themeToggle) themeToggle.innerHTML = '<span class="sr-only">Toggle dark theme</span><i class="fas fa-sun"></i>';
		} else {
			body.classList.remove('dark-theme');
			if(themeToggle) themeToggle.setAttribute('aria-pressed','false');
			if(themeToggle) themeToggle.innerHTML = '<span class="sr-only">Toggle dark theme</span><i class="fas fa-moon"></i>';
		}
	}

	// initialize theme: priority localStorage, default to dark when no preference
	(function initTheme(){
		const stored = localStorage.getItem('theme');
		if(stored){
			applyTheme(stored);
		} else {
			// default to dark for all pages when the user has no stored preference
			applyTheme('dark');
			// persist default so subsequent loads are consistent
			localStorage.setItem('theme', 'dark');
		}
	})();

	if(themeToggle){
		themeToggle.addEventListener('click', ()=>{
			const isDark = body.classList.contains('dark-theme');
			const next = isDark ? 'light' : 'dark';
			applyTheme(next);
			localStorage.setItem('theme', next);
		});
	}
});
