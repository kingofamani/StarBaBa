document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = ''; // 空字串代表相對路徑
    const subscriptionList = document.getElementById('subscription-list');
    const subscriptionForm = document.getElementById('subscription-form');
    const modal = document.getElementById('subscription-modal');
    const modalTitle = document.getElementById('modal-title');
    const addSubscriptionBtn = document.getElementById('add-subscription-btn');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const cancelFormBtn = document.getElementById('cancel-form-btn');

    // 表單欄位
    const formFields = {
        id: document.getElementById('subscription-id'),
        serviceName: document.getElementById('serviceName'),
        predefinedServices: document.getElementById('predefinedServices'),
        serviceIcon: document.getElementById('serviceIcon'),
        tags: document.getElementById('tags'),
        startDate: document.getElementById('startDate'),
        billingCycle: document.getElementById('billingCycle'),
        billingDayOfMonth: document.getElementById('billingDayOfMonth'),
        billingDateOfYear: document.getElementById('billingDateOfYear'),
        price: document.getElementById('price'),
        currency: document.getElementById('currency'),
        paymentMethod: document.getElementById('paymentMethod'),
        paymentCardLastFour: document.getElementById('paymentCardLastFour'),
        paymentCardBank: document.getElementById('paymentCardBank'),
        notes: document.getElementById('notes'),
        isActive: document.getElementById('isActive')
    };
    const dayOfMonthGroup = document.getElementById('dayOfMonthInputGroup');
    const dateOfYearGroup = document.getElementById('dateOfYearInputGroup');
    const paymentDetailsContainer = document.getElementById('paymentDetailsContainer');

    // 統計區域元素
    const statsMonthlyCostEl = document.getElementById('stats-monthly-cost');
    const statsYearlyCostEl = document.getElementById('stats-yearly-cost');
    const statsActiveCountEl = document.getElementById('stats-active-count');
    const statsEquivalencyEl = document.getElementById('stats-equivalency');
    console.log('statsEquivalencyEl initialized:', statsEquivalencyEl); // 新增日誌

    let appSettings = {}; // 儲存從 /api/settings 獲取的設定

    // --- Helper Functions ---
    async function fetchAPI(endpoint, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            }
        };
        const config = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...(options.headers || {}),
            },
        };
        try {
            const response = await fetch(`${API_BASE_URL}/api${endpoint}`, config);
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ error: `HTTP error! status: ${response.status}` }));
                console.error('API Error:', errorData);
                alert(`操作失敗: ${errorData.error || response.statusText}`);
                return null;
            }
            if (response.status === 204) { // No Content
                return true; 
            }
            return await response.json();
        } catch (error) {
            console.error('Fetch Error:', error);
            alert('網路請求錯誤，請檢查主控台。');
            return null;
        }
    }

    function formatDate(dateString) {
        if (!dateString) return 'N/A';
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('zh-TW', { year: 'numeric', month: '2-digit', day: '2-digit' });
        } catch (e) {
            return dateString; // 如果格式不對，直接回傳原始字串
        }
    }
    
    function formatDateTime(dateTimeString) {
        if (!dateTimeString) return 'N/A';
        try {
            const date = new Date(dateTimeString);
            return date.toLocaleString('zh-TW', { year: 'numeric', month: '2-digit', day: '2-digit', hour:'2-digit', minute:'2-digit' });
        } catch (e) {
            return dateTimeString;
        }
    }

    // --- Populate Form Selects ---
    function populateSelect(selectElement, optionsArray, valueField, labelField, addEmptyOption = true) {
        if (!selectElement) return;
        selectElement.innerHTML = ''; // 清空現有選項
        if (addEmptyOption) {
            const emptyOpt = document.createElement('option');
            emptyOpt.value = '';
            emptyOpt.textContent = '請選擇...';
            selectElement.appendChild(emptyOpt);
        }
        optionsArray.forEach(option => {
            const opt = document.createElement('option');
            opt.value = option[valueField];
            opt.textContent = option[labelField];
            selectElement.appendChild(opt);
        });
    }

    function populateFormWithOptions(settings) {
        appSettings = settings; // 保存設定供後續使用
        populateSelect(formFields.billingCycle, settings.billingCycles || [], 'value', 'label');
        populateSelect(formFields.currency, settings.currencies || [], 'code', 'name', false); // 貨幣通常不需「請選擇」
        // 設定預設貨幣
        if (settings.defaultCurrency && formFields.currency) {
            formFields.currency.value = settings.defaultCurrency;
        }
        populateSelect(formFields.tags, (settings.availableTags || []).map(tag => ({ value: tag, label: tag })), 'value', 'label', false);
        populateSelect(formFields.paymentMethod, settings.paymentMethods || [], 'value', 'label');
        
        if (formFields.predefinedServices && settings.predefinedServices) {
            formFields.predefinedServices.innerHTML = '<option value="">或選擇預設服務...</option>'; // Reset
            settings.predefinedServices.forEach(service => {
                const opt = document.createElement('option');
                opt.value = service.name; // 用服務名稱作為 value，方便後續查找
                opt.textContent = service.name;
                opt.dataset.icon = service.icon || '';
                opt.dataset.defaultTags = JSON.stringify(service.defaultTags || []);
                formFields.predefinedServices.appendChild(opt);
            });
        }
    }

    // --- Render Subscriptions ---
    function renderSubscriptionItem(sub) {
        const currencyInfo = (appSettings.currencies || []).find(c => c.code === sub.currency) || { symbol: sub.currency };
        const billingCycleInfo = (appSettings.billingCycles || []).find(bc => bc.value === sub.billingCycle) || { label: sub.billingCycle };
        const paymentMethodInfo = (appSettings.paymentMethods || []).find(pm => pm.value === sub.paymentMethod) || { label: sub.paymentMethod };

        let icon_url = '/static/images/default_icon.svg'; // Default icon

        if (sub.serviceIcon) {
            if (sub.serviceIcon.startsWith('http') || sub.serviceIcon.startsWith('/')) {
                icon_url = sub.serviceIcon; // Absolute URL or root-relative path
            } else {
                icon_url = `/static/${sub.serviceIcon}`; // Path relative to /static/
            }
        } else {
            const predefined = (appSettings.predefinedServices || []).find(ps => ps.name === sub.serviceName);
            if (predefined && predefined.icon) {
                if (predefined.icon.startsWith('http') || predefined.icon.startsWith('/')) {
                    icon_url = predefined.icon;
                } else {
                    icon_url = `/static/${predefined.icon}`; // Path relative to /static/
                }
            }
        }
        
        return `
        <div class="bg-white shadow-md rounded-lg p-6 subscription-card transform hover:scale-105 transition-transform duration-300 ease-in-out" data-id="${sub.id}">
            <div class="flex items-center mb-4">
                <img src="${icon_url}" alt="${sub.serviceName}" class="w-12 h-12 mr-4 rounded-full object-contain p-1 border" onerror="this.onerror=null; this.src='/static/images/default_icon.svg'; this.alt='Default Icon'">
                <div>
                    <h3 class="text-xl font-semibold text-gray-800">${sub.serviceName}</h3>
                    <p class="text-sm text-gray-500">${(sub.tags && sub.tags.length) ? sub.tags.join(', ') : '無標籤'}</p>
                </div>
            </div>
            <div class="space-y-2 text-sm mb-4">
                <p><span class="font-medium text-gray-600">價格:</span> <span class="font-bold text-green-600">${currencyInfo.symbol}${sub.price}</span> / ${billingCycleInfo.label}</p>
                <p><span class="font-medium text-gray-600">開始日期:</span> ${formatDate(sub.startDate)}</p>
                ${sub.billingCycle === 'monthly' && sub.billingDetails && sub.billingDetails.dayOfMonth ? 
                    `<p><span class="font-medium text-gray-600">每月扣款日:</span> 第 ${sub.billingDetails.dayOfMonth} 天</p>` : ''}
                ${sub.billingCycle === 'yearly' && sub.billingDetails && sub.billingDetails.dateOfYear ? 
                    `<p><span class="font-medium text-gray-600">每年扣款日:</span> ${sub.billingDetails.dateOfYear}</p>` : ''}
                <p><span class="font-medium text-gray-600">付款方式:</span> ${paymentMethodInfo.label || '未指定'}</p>
                ${sub.paymentDetails && sub.paymentDetails.cardLastFour ? 
                    `<p><span class="font-medium text-gray-600">卡號末四碼:</span> ${sub.paymentDetails.cardLastFour}</p>` : ''}
                ${sub.paymentDetails && sub.paymentDetails.cardBank ? 
                    `<p><span class="font-medium text-gray-600">發卡銀行:</span> ${sub.paymentDetails.cardBank}</p>` : ''}
                ${sub.notes ? `<p><span class="font-medium text-gray-600">備註:</span> <span class="text-gray-700">${sub.notes.substring(0,50)}${sub.notes.length > 50 ? '...':''}</span></p>` : ''}
                <p><span class="font-medium text-gray-600">狀態:</span> 
                    <span class="${sub.isActive ? 'text-green-500' : 'text-red-500'} font-semibold">
                        ${sub.isActive ? '啟用中' : '已停用'}
                    </span>
                </p>
            </div>
            <div class="flex justify-end space-x-2 border-t pt-4 mt-4">
                <button class="edit-btn bg-yellow-500 hover:bg-yellow-600 text-white text-xs font-bold py-2 px-3 rounded focus:outline-none focus:shadow-outline" data-id="${sub.id}">編輯</button>
                <button class="delete-btn bg-red-500 hover:bg-red-600 text-white text-xs font-bold py-2 px-3 rounded focus:outline-none focus:shadow-outline" data-id="${sub.id}" data-name="${sub.serviceName}">刪除</button>
            </div>
            <div class="text-xs text-gray-400 mt-2 text-right">
                <p>ID: ${sub.id.substring(0,8)}...</p>
                <p>更新於: ${formatDateTime(sub.updatedAt)}</p>
            </div>
        </div>
        `;
    }

    async function loadAndRenderSubscriptions() {
        const subscriptions = await fetchAPI('/subscriptions');
        if (subscriptionList && subscriptions) {
            if (subscriptions.length === 0) {
                subscriptionList.innerHTML = '<p class="text-gray-500 italic col-span-full">目前沒有訂閱項目，快來新增一個吧！</p>';
            } else {
                subscriptionList.innerHTML = subscriptions.map(renderSubscriptionItem).join('');
            }
            addEventListenersToButtons(); // 新增完卡片後綁定事件
        } else if (subscriptionList) {
            subscriptionList.innerHTML = '<p class="text-red-500 italic col-span-full">無法載入訂閱項目，請稍後再試。</p>';
        }
        await loadAndRenderStats(); // 訂閱更新後，重新計算統計
    }

    // --- Render Stats ---
    async function loadAndRenderStats() {
        const stats = await fetchAPI('/stats');
        console.log('Stats fetched for loadAndRenderStats:', stats); // 新增日誌
        if (stats && statsMonthlyCostEl && statsYearlyCostEl && statsActiveCountEl && statsEquivalencyEl) {
            const currencyInfo = (appSettings.currencies || []).find(c => c.code === stats.currency) || { symbol: stats.currency };
            statsMonthlyCostEl.textContent = `${currencyInfo.symbol} ${stats.totalMonthlyCost.toLocaleString()}`;
            statsYearlyCostEl.textContent = `${currencyInfo.symbol} ${stats.totalYearlyCost.toLocaleString()}`;
            statsActiveCountEl.textContent = stats.activeSubscriptionsCount;
            
            renderStatistics(stats);
        } else if (statsEquivalencyEl) {
             console.log('Failed to load full stats or some elements missing, updating statsEquivalencyEl with error.'); // 新增日誌
             statsEquivalencyEl.innerHTML = '<h3 class="text-lg font-semibold text-gray-700 mb-2">月費約等於...</h3><p class="text-sm text-red-500 italic">無法載入統計數據。</p>';
        } else {
            console.error('statsEquivalencyEl is not defined, cannot update stats.'); // 新增日誌
        }
    }

    function renderStatistics(stats) {
        console.log('renderStatistics called with data:', stats, 'Targeting element:', statsEquivalencyEl);
        if (statsEquivalencyEl) {
            if (stats.equivalency && stats.equivalency.length > 0) {
                console.log('Rendering equivalency items:', stats.equivalency);

                let html = '<p class="text-sm text-gray-600 dark:text-gray-400">您的總月費約可換算成：</p><ul class="mt-2 space-y-3 max-w-full">';

                stats.equivalency.forEach((item, index) => {
                    // item.count 已經是後端 round(float, 2) 過的數字
                    // item.countInt 是後端 int(float) 過的整數
                    const itemId = `equiv-item-${index}`;

                    html += `<li class="w-full flex flex-col items-start py-3 pr-3 pl-0 bg-gray-50 dark:bg-gray-700 rounded-lg shadow-sm">
                                <div class="text-md font-medium text-gray-800 dark:text-gray-200 mb-2">
                                    ${item.count.toFixed(2)} ${item.unit} ${item.itemName}
                                </div>`;

                    if (item.imagePath && item.countInt > 0) {
                        // 外層容器
                        html += '<div class="w-full mt-1">';
                        
                        // 第一行：固定顯示最多10個圖示
                        const firstRowCount = Math.min(item.countInt, 10); 
                        html += '<div class="flex flex-wrap gap-1 mb-1">';
                        
                        for (let i = 0; i < firstRowCount; i++) {
                            html += `<img 
                                src="/${item.imagePath.startsWith('static/') ? '' : 'static/'}${item.imagePath}" 
                                alt="${item.imageUnit || item.itemName}" 
                                class="h-6 w-6 object-contain" 
                                title="${item.itemName}">`;
                        }
                        
                        if (item.countInt > 10) {
                            html += `<button id="toggle-${itemId}" class="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200 focus:outline-none ml-1" data-expanded="false">
                                        顯示全部(${item.countInt})
                                    </button>`;
                        }
                        
                        html += '</div>';
                        
                        // 如果有更多圖示，創建可折疊區域
                        if (item.countInt > 10) {
                            html += `<div id="${itemId}" class="hidden mt-2">`;
                            
                            // 處理剩餘的圖示，每10個一組，最多到總共50個
                            const startIndexForExpansion = 10; // 從第11個圖示開始
                            const maxTotalImagesToShow = 50;   // 總共最多顯示50個圖示 (10個初始 + 40個展開)
                            const endIndexForExpansion = Math.min(item.countInt, maxTotalImagesToShow);

                            for (let i = startIndexForExpansion; i < endIndexForExpansion; i += 10) {
                                html += '<div class="flex flex-wrap gap-1 mb-1">'; // 每10個圖示一組新的div
                                const endOfCurrentChunk = Math.min(i + 10, endIndexForExpansion);
                                for (let j = i; j < endOfCurrentChunk; j++) {
                                    html += `<img 
                                        src="/${item.imagePath.startsWith('static/') ? '' : 'static/'}${item.imagePath}" 
                                        alt="${item.imageUnit || item.itemName}" 
                                        class="h-6 w-6 object-contain" 
                                        title="${item.itemName}">`;
                                }
                                html += '</div>'; // 結束這一組10個圖示的div
                            }
                            
                            if (item.countInt > maxTotalImagesToShow) {
                                html += '<span class="text-xs text-gray-500 dark:text-gray-300 self-center ml-1">...等</span>';
                            }
                            
                            html += '</div>'; // 結束可折疊區域的div
                        }
                        
                        html += '</div>';  // 結束外層容器
                    }
                    html += '</li>';
                });

                html += '</ul>';
                statsEquivalencyEl.innerHTML = html;
                
                // 添加展開/收合按鈕的事件處理
                stats.equivalency.forEach((item, index) => {
                    if (item.countInt > 10) {
                        const itemId = `equiv-item-${index}`;
                        const toggleBtn = document.getElementById(`toggle-${itemId}`);
                        const contentDiv = document.getElementById(itemId);
                        
                        if (toggleBtn && contentDiv) {
                            toggleBtn.addEventListener('click', function() {
                                const isExpanded = this.getAttribute('data-expanded') === 'true';
                                if (isExpanded) {
                                    contentDiv.classList.add('hidden');
                                    this.textContent = `顯示全部(${item.countInt})`;
                                    this.setAttribute('data-expanded', 'false');
                                } else {
                                    contentDiv.classList.remove('hidden');
                                    this.textContent = '收合';
                                    this.setAttribute('data-expanded', 'true');
                                }
                            });
                        }
                    }
                });
            } else {
                console.log('No equivalency items to render, or stats.equivalency is empty.');
                statsEquivalencyEl.innerHTML = '<p class="text-sm text-gray-600 dark:text-gray-400">目前無換算資料。</p>';
            }
        } else {
            console.error('renderStatistics: statsEquivalencyEl is not defined!');
        }
    }

    // --- Form Handling ---
    function openSubscriptionModal(subscription = null) {
        subscriptionForm.reset();
        formFields.id.value = ''; // 清空 ID
        
        // 重置 billing cycle 相關的顯示
        if(dayOfMonthGroup) dayOfMonthGroup.style.display = 'none';
        if(dateOfYearGroup) dateOfYearGroup.style.display = 'none';
        if(formFields.billingDayOfMonth) formFields.billingDayOfMonth.required = false;
        if(formFields.billingDateOfYear) formFields.billingDateOfYear.required = false;
        if(paymentDetailsContainer) paymentDetailsContainer.style.display = 'none';

        if (subscription) {
            modalTitle.textContent = '編輯訂閱';
            formFields.id.value = subscription.id;
            formFields.serviceName.value = subscription.serviceName || '';
            formFields.serviceIcon.value = subscription.serviceIcon || '';
            // 設定多選 select (tags)
            if (formFields.tags && subscription.tags) {
                Array.from(formFields.tags.options).forEach(option => {
                    option.selected = subscription.tags.includes(option.value);
                });
            }
            formFields.startDate.value = subscription.startDate ? subscription.startDate.split('T')[0] : '';
            formFields.billingCycle.value = subscription.billingCycle || '';
            handleBillingCycleChange(); // 觸發一次以顯示正確的 billingDetails
            if (subscription.billingDetails) {
                if (subscription.billingDetails.dayOfMonth) {
                    formFields.billingDayOfMonth.value = subscription.billingDetails.dayOfMonth;
                }
                if (subscription.billingDetails.dateOfYear) {
                    formFields.billingDateOfYear.value = subscription.billingDetails.dateOfYear;
                }
            }
            formFields.price.value = subscription.price || '';
            formFields.currency.value = subscription.currency || appSettings.defaultCurrency || '';
            formFields.paymentMethod.value = subscription.paymentMethod || '';
            handlePaymentMethodChange(); // 觸發一次以顯示正確的 paymentDetails
            if (subscription.paymentDetails) {
                 formFields.paymentCardLastFour.value = subscription.paymentDetails.cardLastFour || '';
                 formFields.paymentCardBank.value = subscription.paymentDetails.cardBank || '';
            }
            formFields.notes.value = subscription.notes || '';
            formFields.isActive.checked = subscription.isActive === undefined ? true : subscription.isActive;
        } else {
            modalTitle.textContent = '新增訂閱';
            formFields.isActive.checked = true; // 新增時預設啟用
            if (appSettings.defaultCurrency && formFields.currency) {
                 formFields.currency.value = appSettings.defaultCurrency;
            }
        }
        modal.style.display = 'block';
    }

    function closeSubscriptionModal() {
        modal.style.display = 'none';
    }

    async function handleFormSubmit(event) {
        event.preventDefault();
        const formData = new FormData(subscriptionForm);
        const data = {};
        const billingDetails = {};
        const paymentDetails = {};

        // FormData 處理多選 select 和 checkbox
        data.tags = formData.getAll('tags');
        data.isActive = formFields.isActive.checked; // 直接從 checkbox 元素獲取狀態
        
        formData.forEach((value, key) => {
            if (key === 'tags' || key === 'isActive') return; // 已單獨處理

            if (key.startsWith('billingDetails.')) {
                billingDetails[key.split('.')[1]] = value;
            } else if (key.startsWith('paymentDetails.')) {
                paymentDetails[key.split('.')[1]] = value;
            } else {
                data[key] = value;
            }
        });

        if (Object.keys(billingDetails).length > 0) {
            data.billingDetails = billingDetails;
        }
        if (Object.keys(paymentDetails).length > 0) {
            data.paymentDetails = paymentDetails;
        }

        // 確保 price 是數字
        if (data.price) {
            data.price = parseFloat(data.price);
            if (isNaN(data.price)) {
                alert('價格必須是有效的數字。');
                return;
            }
        }
        // 清理 billingDetails 中不必要的空值
        if (data.billingCycle !== 'monthly' && data.billingDetails && data.billingDetails.dayOfMonth) {
            delete data.billingDetails.dayOfMonth;
        }
        if (data.billingCycle !== 'yearly' && data.billingDetails && data.billingDetails.dateOfYear) {
            delete data.billingDetails.dateOfYear;
        }
        if (data.billingDetails && Object.keys(data.billingDetails).length === 0) {
             delete data.billingDetails;
        }
        
        // 清理 paymentDetails 中不必要的空值
        if (data.paymentMethod !== 'credit_card' && data.paymentDetails) {
            if (data.paymentDetails.cardLastFour) delete data.paymentDetails.cardLastFour;
            if (data.paymentDetails.cardBank) delete data.paymentDetails.cardBank;
        }
        if (data.paymentDetails && Object.keys(data.paymentDetails).length === 0) {
             delete data.paymentDetails;
        }

        const id = formFields.id.value;
        let result;
        if (id) { // 更新
            result = await fetchAPI(`/subscriptions/${id}`, { method: 'PUT', body: JSON.stringify(data) });
        } else { // 新增
            result = await fetchAPI('/subscriptions', { method: 'POST', body: JSON.stringify(data) });
        }

        if (result) {
            closeSubscriptionModal();
            await loadAndRenderSubscriptions(); // 重新載入列表和統計
            alert(id ? '訂閱更新成功！' : '訂閱新增成功！');
        }
    }
    
    // 當預選服務改變時，自動填充服務名稱、圖示和標籤
    if (formFields.predefinedServices) {
        formFields.predefinedServices.addEventListener('change', (event) => {
            const selectedOption = event.target.selectedOptions[0];
            if (!selectedOption || !selectedOption.value) return;

            const serviceName = selectedOption.value;
            const icon = selectedOption.dataset.icon;
            const defaultTags = JSON.parse(selectedOption.dataset.defaultTags || '[]');

            formFields.serviceName.value = serviceName;
            if (icon) formFields.serviceIcon.value = icon;
            
            if (formFields.tags && defaultTags.length > 0) {
                Array.from(formFields.tags.options).forEach(option => {
                    option.selected = defaultTags.includes(option.value);
                });
            }
        });
    }

    // --- Dynamic Form Fields Logic ---
    function handleBillingCycleChange() {
        if (!formFields.billingCycle || !dayOfMonthGroup || !dateOfYearGroup) return;
        const cycle = formFields.billingCycle.value;
        dayOfMonthGroup.style.display = cycle === 'monthly' ? 'block' : 'none';
        formFields.billingDayOfMonth.required = cycle === 'monthly';
        dateOfYearGroup.style.display = cycle === 'yearly' ? 'block' : 'none';
        formFields.billingDateOfYear.required = cycle === 'yearly';
    }

    function handlePaymentMethodChange() {
        if (!formFields.paymentMethod || !paymentDetailsContainer) return;
        const method = formFields.paymentMethod.value;
        // 假設只有 credit_card 需要額外欄位
        paymentDetailsContainer.style.display = method === 'credit_card' ? 'block' : 'none';
    }

    // --- Event Listeners ---
    function addEventListenersToButtons() {
        document.querySelectorAll('.edit-btn').forEach(button => {
            button.addEventListener('click', async (e) => {
                const id = e.target.dataset.id;
                const subscription = await fetchAPI(`/subscriptions/${id}`);
                if (subscription) {
                    openSubscriptionModal(subscription);
                }
            });
        });

        document.querySelectorAll('.delete-btn').forEach(button => {
            button.addEventListener('click', async (e) => {
                const id = e.target.dataset.id;
                const name = e.target.dataset.name || '此項目';
                if (confirm(`您確定要刪除「${name}」嗎？此操作無法復原。`)) {
                    const success = await fetchAPI(`/subscriptions/${id}`, { method: 'DELETE' });
                    if (success) {
                        await loadAndRenderSubscriptions(); // 重新載入列表和統計
                        alert('訂閱已刪除。');
                    }
                }
            });
        });
    }

    if (addSubscriptionBtn) addSubscriptionBtn.addEventListener('click', () => openSubscriptionModal());
    if (closeModalBtn) closeModalBtn.addEventListener('click', closeSubscriptionModal);
    if (cancelFormBtn) cancelFormBtn.addEventListener('click', closeSubscriptionModal);
    if (subscriptionForm) subscriptionForm.addEventListener('submit', handleFormSubmit);
    if (formFields.billingCycle) formFields.billingCycle.addEventListener('change', handleBillingCycleChange);
    if (formFields.paymentMethod) formFields.paymentMethod.addEventListener('change', handlePaymentMethodChange);

    // 點擊 Modal 外部區域關閉 Modal (已在 index.html 中處理，但保留此處作為備用)
    // window.addEventListener('click', (event) => {
    //     if (event.target == modal) {
    //         closeSubscriptionModal();
    //     }
    // });

    // --- Initial Load ---
    async function initializeApp() {
        const settings = await fetchAPI('/settings');
        if (settings) {
            populateFormWithOptions(settings);
            await loadAndRenderSubscriptions(); // 載入訂閱前先載入設定，因為渲染卡片時會用到設定檔
            // loadAndRenderStats(); // loadAndRenderSubscriptions 內部會呼叫
        } else {
            alert('無法載入應用程式設定，部分功能可能無法正常運作。');
            if(subscriptionList) subscriptionList.innerHTML = '<p class="text-red-500 italic col-span-full">無法載入應用程式設定，請稍後再試。</p>';
            if(statsEquivalencyEl) statsEquivalencyEl.innerHTML = '<h3 class="text-lg font-semibold text-gray-700 mb-2">月費約等於...</h3><p class="text-sm text-red-500 italic">無法載入應用程式設定。</p>';
        }
    }

    initializeApp();
}); 