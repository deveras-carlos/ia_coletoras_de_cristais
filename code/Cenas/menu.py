from parametros import Parametro
from dataclasses import fields

def menu_terminal(parametros: Parametro):
    """Menu de terminal para editar os valores de Parametro."""
    while True:

        print("\n==== Menu de Configuração ====")
        for i, field in enumerate(fields(parametros)):
            value = getattr(parametros, field.name)
            print(f"{i + 1}. {field.name} (atual: {value})")
        
        print(f"{len(fields(parametros)) + 1}. Salvar e sair")

        try:
            choice = int(input("\nEscolha uma opção para editar (ou salvar e sair): "))
            if choice == len(fields(parametros)) + 1:
                print("Parâmetros salvos:")
                print(parametros)
                break
            elif 1 <= choice <= len(fields(parametros)):
                selected_field = fields(parametros)[choice - 1]
                current_value = getattr(parametros, selected_field.name)
                new_value = input(
                    f"Digite o novo valor para {selected_field.name} (atual: {current_value}): "
                )
                try:
                    # Tenta converter o valor para o tipo apropriado
                    casted_value = type(current_value)(new_value)
                    setattr(parametros, selected_field.name, casted_value)
                except ValueError:
                    print("Entrada inválida! O valor não foi alterado.")
            else:
                print("Opção inválida! Tente novamente.")
        except ValueError:
            print("Entrada inválida! Por favor, insira um número.")
    return parametros