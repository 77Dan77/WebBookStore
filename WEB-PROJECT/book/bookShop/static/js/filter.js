function ajaxSend(url, params) {
    // Отправляем запрос
    fetch(`${url}?${params}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => response.json())
        .then(json => render(json))
        .catch(error => console.error(error))
}


const forms = document.querySelector('form[name=filter]');

forms.addEventListener('submit', function (e) {
    // Получаем данные из формы
    e.preventDefault();
    let url = this.action;
    let params = new URLSearchParams(new FormData(this)).toString();
    ajaxSend(url, params);
});

function render(data) {
    // Рендер шаблона
    let template = Hogan.compile(html);
    let output = template.render(data);

    const div = document.querySelector('.markerclass>.row');
    div.innerHTML = output;
}

let html = '\
{{#books}}\
   <div style="margin:0px; margin-top: 10px;margin-left:2.5%; background-color: #B8680A;">
           <a href="/{{ url }}">
           <img style="padding: 5px; height: 420px; width: 220px" src="Media/books/{{ image }}" class="pictures1" style="height: 291px; width: 197px" alt="BookShop"></a>
             {% if name|length|get_digit:"-1" < 9 %}
                  <p style="font-family: Rosarivo;font-style: normal;font-weight: normal;font-size: 22px;line-height: 34px;text-align: center; color: #FFFFFF;">
                  {{name}}</p>
             {% else %}
                   <p style="font-family: Rosarivo;font-style: normal;font-weight: normal;font-size: 22px;line-height: 34px;text-align: center; color: #FFFFFF;">
                   {{name|slice:":9"|add:" ..."}}</p>
             {% endif %}
                   <p style="font-family: Rosarivo;font-style: normal;font-weight: normal;font-size: 16px;line-height: 34px; margin-top: -20px; margin-left: 10px; color: #FFFFFF;">
             {% for author in authors.all %}

             {% if author.name|length|get_digit:"-1" < 9 %}
             {{author.name|slice:":8"}}

              {% else %}
               {{author.name|slice:":5"|add:" ..."}}
              {% endif %}
              {% endfor %}
                     </p>
                        <p style="font-family: Rosarivo;font-style: normal;font-weight: normal;font-size: 12px;line-height: 34px; text-align: right; margin-top: -25px; margin-right: 10px; color: #FFFFFF;">
                           {{money}}
                            $
                           </p>
                             <p class="Cart" style="font-family: Rosarivo;font-style: normal;font-weight: normal;font-size: 16px;line-height: 34px; text-align: center; color: #131111;">Add to Cart</p>
                           </div>
{{/books}}'

