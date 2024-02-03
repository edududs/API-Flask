from typing import Union

import requests


class APIHandler:
    BASE_URL = "http://localhost:5000"

    def show_products(self):
        response = requests.get(f"{self.BASE_URL}/products", timeout=100)
        return response.json()

    def create_product(self, name, description):
        response = requests.post(
            f"{self.BASE_URL}/products",
            json={"name": name, "description": description},
            timeout=100,
        )
        return response.json()

    def delete_product(self, product_id):
        response = requests.delete(f"{self.BASE_URL}/product/{product_id}", timeout=100)
        return response.json()

    def create_user(self, name, email, password):
        response = requests.post(
            f"{self.BASE_URL}/users",
            json={"name": name, "email": email, "password": password},
            timeout=100,
        )
        return response.json()

    def show_users(self):
        response = requests.get(f"{self.BASE_URL}/users", timeout=100)
        return response.json()

    def delete_user(self, user_id):
        response = requests.delete(f"{self.BASE_URL}/user/{user_id}", timeout=100)
        return response.json()

    def show_user_products(self, user_id):
        response = requests.get(f"{self.BASE_URL}/user/{user_id}/products", timeout=100)
        return response.json()

    def assign_product_to_user(self, user_id, product_id):
        response = requests.post(
            f"{self.BASE_URL}/user/{user_id}/assign_product/{product_id}",
            timeout=100,
        )
        return response.json()

    def update_user(self, user_id, name, email, password):
        response = requests.put(
            f"{self.BASE_URL}/user/{user_id}",
            json={"name": name, "email": email, "password": password},
            timeout=100,
        )
        return response.json()

    def update_product(self, product_id, name, description):
        response = requests.put(
            f"{self.BASE_URL}/product/{product_id}",
            json={"name": name, "description": description},
            timeout=100,
        )
        return response.json()


# Função para criar uma interface de linha de comando para interagir com a API
# Defina a função main
def main():
    # Instância do APIHandler
    api_handler = APIHandler()

    while True:
        print("\nEscolha uma opção:")
        print("1. Mostrar todos os produtos")
        print("2. Criar um novo produto")
        print("3. Deletar um produto")
        print("4. Mostrar todos os usuários")
        print("5. Criar um novo usuário")
        print("6. Deletar um usuário")
        print("7. Mostrar produtos de um usuário")
        print("8. Atribuir produto a usuário")
        print("9. Atualizar um usuário")
        print("10. Atualizar um produto")
        print("0. Sair")

        option = input("Opção: ")

        match option:
            case "1":
                print(api_handler.show_products())
            case "2":
                name = input("Nome do produto: ")
                description = input("Descrição do produto: ")
                print(api_handler.create_product(name, description))
            case "3":
                product_id = input("ID do produto a ser deletado: ")
                print(api_handler.delete_product(product_id))
            case "4":
                print(api_handler.show_users())
            case "5":
                name = input("Nome do usuário: ")
                email = input("Email do usuário: ")
                password = input("Senha do usuário: ")
                print(api_handler.create_user(name, email, password))
            case "6":
                user_id = input("ID do usuário a ser deletado: ")
                print(api_handler.delete_user(user_id))
            case "7":
                user_id = input("ID do usuário: ")
                print(api_handler.show_user_products(user_id))
            case "8":
                user_id = input("ID do usuário: ")
                product_id = input("ID do produto: ")
                print(api_handler.assign_product_to_user(user_id, product_id))
            case "9":
                user_id = input("ID do usuário: ")
                name = input("Novo nome do usuário: ")
                email = input("Novo email do usuário: ")
                password = input("Nova senha do usuário: ")
                print(api_handler.update_user(user_id, name, email, password))
            case "10":
                product_id = input("ID do produto: ")
                name = input("Novo nome do produto: ")
                description = input("Nova descrição do produto: ")
                print(api_handler.update_product(product_id, name, description))
            case "0":
                print("Saindo...")
                break
            case _:
                print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
