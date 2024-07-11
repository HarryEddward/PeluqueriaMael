import yaml

class Ansible:
    @classmethod
    def load_yml(cls, file_path='servers.yml') -> dict:
        """
        Carga un archivo YAML y devuelve su contenido como un diccionario.
        
        Args:
            file_path (str): Ruta del archivo YAML a cargar.

        Returns:
            dict: Contenido del archivo YAML.

        Raises:
            FileNotFoundError: Si el archivo no se encuentra.
            yaml.YAMLError: Si hay un error al cargar el YAML.
        """
        try:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo {file_path} no se encuentra.")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error al cargar el archivo YAML: {e}")

    @classmethod
    def generate_host_config(cls, servers: dict) -> str:
        """
        Genera la configuración del archivo hosts.ini a partir del diccionario de servidores.

        Args:
            servers (dict): Diccionario con la configuración de los servidores.

        Returns:
            str: Configuración formateada para hosts.ini.
        """
        config_lines = []
        
        for name_section, section in servers.items():
            config_lines.append(f'[{name_section}]\n')
            
            if not section:
                raise ValueError(f"No hay elementos dentro de la sección: {name_section}")

            for server_name, ssh in section.items():
                try:
                    name_ssh, ip_ssh = ssh.split('@')
                    config_lines.append(f'{server_name} ansible_host={ip_ssh} user={name_ssh}\n')
                except ValueError:
                    raise ValueError(f"El formato de la configuración de {server_name} en la sección {name_section} es incorrecto.")
            
            config_lines.append('\n')
        
        return ''.join(config_lines)

    @classmethod
    def config(cls, input_path='servers.yml', output_path='../hosts.ini'):
        """
        Carga la configuración del archivo YAML y genera el archivo hosts.ini.

        Args:
            input_path (str): Ruta del archivo YAML de entrada.
            output_path (str): Ruta del archivo hosts.ini de salida.
        """
        configure_file = cls.load_yml(input_path)

        if not configure_file:
            raise ValueError("El archivo de configuración está vacío.")
        
        servers = configure_file.get('servers', {})
        if not servers:
            raise ValueError("No se encontraron servidores en el archivo de configuración.")
        
        host_config = cls.generate_host_config(servers)

        with open(output_path, 'w') as file:
            file.write(host_config)

if __name__ == "__main__":
    Ansible.config()
