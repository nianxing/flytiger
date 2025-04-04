// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化工具提示
    initializeTooltips();
    
    // 初始化产品过滤器
    initializeProductFilter();
    
    // 初始化购物车功能
    initializeCart();
    
    // 初始化表单验证
    initializeFormValidation();
});

// 初始化Bootstrap工具提示
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// 产品筛选功能
function initializeProductFilter() {
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', function(event) {
            event.preventDefault();
            // 这里可以添加筛选逻辑
            console.log('筛选表单已提交');
            
            // 实际应用中应该发送AJAX请求或刷新页面
        });
    }
}

// 购物车功能
function initializeCart() {
    // 添加到购物车按钮
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const productId = this.dataset.productId;
            const quantity = document.getElementById('quantity') ? document.getElementById('quantity').value : 1;
            
            console.log(`添加商品 ${productId} 到购物车，数量: ${quantity}`);
            
            // 显示添加成功消息
            showMessage('商品已成功添加到购物车！', 'success');
            
            // 实际应用中应该发送AJAX请求
        });
    });
    
    // 更新购物车数量
    const quantityInputs = document.querySelectorAll('.quantity-input');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const productId = this.dataset.productId;
            const quantity = this.value;
            
            if (quantity < 1) {
                this.value = 1;
                return;
            }
            
            console.log(`更新商品 ${productId} 的数量为 ${quantity}`);
            
            // 实际应用中应该发送AJAX请求更新购物车并刷新小计和总计
        });
    });
    
    // 从购物车中删除商品
    const removeButtons = document.querySelectorAll('.remove-from-cart');
    removeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            
            if (confirm('确定要从购物车中删除此商品吗？')) {
                console.log(`从购物车中删除商品 ${productId}`);
                
                // 实际应用中应该发送AJAX请求删除商品并刷新购物车
            }
        });
    });
}

// 表单验证
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

// 显示消息提示
function showMessage(message, type = 'info') {
    // 创建消息元素
    const messageDiv = document.createElement('div');
    messageDiv.className = `alert alert-${type} alert-dismissible fade show message-toast`;
    messageDiv.setAttribute('role', 'alert');
    messageDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // 添加样式
    messageDiv.style.position = 'fixed';
    messageDiv.style.top = '20px';
    messageDiv.style.right = '20px';
    messageDiv.style.zIndex = '9999';
    messageDiv.style.maxWidth = '300px';
    
    // 添加到页面
    document.body.appendChild(messageDiv);
    
    // 5秒后自动关闭
    setTimeout(() => {
        messageDiv.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(messageDiv);
        }, 500);
    }, 5000);
}

// 产品图片切换功能
function changeProductImage(imageUrl) {
    const mainImage = document.getElementById('main-product-image');
    if (mainImage) {
        mainImage.src = imageUrl;
    }
}

// 省市联动功能
function updateCities() {
    const province = document.getElementById('province');
    const city = document.getElementById('city');
    
    if (province && city) {
        const provinceValue = province.value;
        
        // 清空城市选项
        city.innerHTML = '<option value="" selected disabled>请选择城市</option>';
        
        // 根据省份设置对应的城市
        if (provinceValue === '广东省') {
            addCityOption(city, '广州市');
            addCityOption(city, '深圳市');
            addCityOption(city, '东莞市');
            addCityOption(city, '佛山市');
        } else if (provinceValue === '北京市') {
            addCityOption(city, '东城区');
            addCityOption(city, '西城区');
            addCityOption(city, '朝阳区');
            addCityOption(city, '海淀区');
        } else if (provinceValue === '上海市') {
            addCityOption(city, '黄浦区');
            addCityOption(city, '徐汇区');
            addCityOption(city, '长宁区');
            addCityOption(city, '静安区');
        }
        
        // 启用城市选择
        city.disabled = false;
    }
}

// 添加城市选项
function addCityOption(selectElement, cityName) {
    const option = document.createElement('option');
    option.value = cityName;
    option.textContent = cityName;
    selectElement.appendChild(option);
} 