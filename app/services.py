from flask import current_app

def calculate_statistics(subscriptions_data, settings_data):
    """
    計算總月費、總年費，並將費用換算成 equivalencyItems 中的商品數量。
    基於 settings_data 中的 defaultCurrency 進行計算。
    """
    total_monthly_cost = 0
    total_yearly_cost = 0
    
    default_currency = settings_data.get('defaultCurrency', 'TWD') # 與 routes.py 中保持一致
    equivalency_items = settings_data.get('equivalencyItems', [])

    active_subscriptions = [s for s in subscriptions_data if s.get('isActive', False)]
    
    for sub in active_subscriptions:
        if sub.get('currency') == default_currency: # MVP 簡化：只計算預設貨幣
            price = sub.get('price', 0)
            try:
                price = float(price) # 確保 price 是數字
            except ValueError:
                current_app.logger.warning(f"Invalid price for subscription {sub.get('serviceName')}: {sub.get('price')}")
                continue

            billing_cycle = sub.get('billingCycle')
            if billing_cycle == 'monthly':
                total_monthly_cost += price
                total_yearly_cost += price * 12
            elif billing_cycle == 'yearly':
                total_yearly_cost += price
                total_monthly_cost += price / 12
            # 'onetime', 'lifetime', 'quarterly', 'weekly' 等在MVP階段暫不計入週期性總費用

    equivalency_results = []
    if equivalency_items and total_monthly_cost > 0:
        for item in equivalency_items:
            item_price = item.get('price')
            item_currency = item.get('currency')
            item_name = item.get('name')
            item_unit = item.get('unit', '個') # 與 routes.py 中保持一致

            if item_currency == default_currency and item_name and isinstance(item_price, (int, float)) and item_price > 0:
                try:
                    count = total_monthly_cost / float(item_price)
                    equivalency_results.append({
                        "itemName": item_name,
                        "count": round(count, 2),
                        "unit": item_unit
                    })
                except ZeroDivisionError: # 理論上 item_price > 0 已經避免了
                    current_app.logger.warning(f"Equivalency item '{item_name}' has price 0, skipping.")
                except Exception as e:
                    current_app.logger.error(f"Error calculating equivalency for '{item_name}': {e}")
            # else:
                # current_app.logger.debug(f"Skipping equivalency item due to missing data, currency mismatch, or invalid price: {item}")
                
    return {
        "totalMonthlyCost": round(total_monthly_cost, 2),
        "totalYearlyCost": round(total_yearly_cost, 2),
        "currency": default_currency,
        "activeSubscriptionsCount": len(active_subscriptions),
        "equivalency": equivalency_results # 與 routes.py 中一致的鍵名
    }

# 你可以在這裡加入其他服務層的函式，例如更複雜的資料分析、提醒生成等。 