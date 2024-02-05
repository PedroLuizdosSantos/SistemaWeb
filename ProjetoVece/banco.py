from ProjetoVece import app, database
from ProjetoVece.models import Usuario, Solicita

 #Comandos para deletar e recriar o Banco de Dados
with app.app_context():
    database.drop_all()
    database.create_all()

 #Comando para verificar os usuarios no Banco de Dados
#with app.app_context():
    #meus_usuarios = Solicita.query.all()
    #print(meus_usuarios)

 #<div class="form-group">
                            #{{ form_solicita.anexo.label }}

                            #{{ form_solicita.anexo(class="form-control-file") }}
                            #{% if form_solicita.anexo.errors %}
                               # {% for erro in form_solicita.anexo.errors %}
                                         #<span class="text-danger"> {{ erro }} </span><br>
                               # {% endfor %}
                            #{% endif %}
                        #</div>