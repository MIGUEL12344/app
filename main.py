from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup

class InputScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Crear el diseño principal
        layout = BoxLayout(orientation='vertical')
        
        # Solicitar al usuario que ingrese sus datos
        self.name_input = TextInput(hint_text="Nombre")
        self.last_name_input = TextInput(hint_text="Apellidos")
        self.career_input = TextInput(hint_text="Carrera")
        self.cycle_input = TextInput(hint_text="Ciclo")
        
        layout.add_widget(self.name_input)
        layout.add_widget(self.last_name_input)
        layout.add_widget(self.career_input)
        layout.add_widget(self.cycle_input)
        
        # Género con botones de opción
        gender_label = Label(text="Género:")
        layout.add_widget(gender_label)
        self.gender_buttons = []
        gender_options = ["Masculino", "Femenino"]
        gender_layout = BoxLayout(orientation='horizontal')
        for option in gender_options:
            button = Button(text=option, on_press=self.select_gender)
            self.gender_buttons.append(button)
            gender_layout.add_widget(button)
            if len(gender_layout.children) == 2:
                layout.add_widget(gender_layout)
                gender_layout = BoxLayout(orientation='horizontal')
        
        # Botón para confirmar los datos
        confirm_button = Button(text="Confirmar", on_press=self.switch_to_image_screen)
        layout.add_widget(confirm_button)
        
        self.add_widget(layout)
        
    def select_gender(self, instance):
        for button in self.gender_buttons:
            button.background_color = (1, 1, 1, 1)  # Restaurar color de fondo predeterminado
        instance.background_color = (0, 1, 0, 1)  # Cambiar color de fondo del botón seleccionado
    
    def switch_to_image_screen(self, instance):
        if not self.name_input.text or not self.last_name_input.text or not self.career_input.text or not self.cycle_input.text:
            # Mostrar mensaje de error si falta algún campo
            self.show_error_dialog("Por favor, complete todos los campos.")
        else:
            gender = None
            for button in self.gender_buttons:
                if button.background_color == (0, 1, 0, 1):
                    gender = button.text
                    break
            App.get_running_app().image_screen.update_data(
                self.name_input.text,
                self.last_name_input.text,
                self.career_input.text,
                self.cycle_input.text,
                gender
            )
            App.get_running_app().screen_manager.current = "image"
    
    def show_error_dialog(self, message):
        # Crear y mostrar un diálogo emergente con el mensaje de error
        popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

class ImageScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Crear el diseño principal
        layout = BoxLayout(orientation='vertical')
        
        # Widget de imagen
        self.img = Image()
        layout.add_widget(self.img)
        
        self.add_widget(layout)
    
    def update_data(self, name, last_name, career, cycle, gender):
        # Ruta de la imagen
        image_path = "bembi.jpeg"
        
        # Mostrar la imagen
        self.img.source = image_path
        self.img.allow_stretch = True  # Permitir estiramiento de la imagen para llenar el widget de imagen

class MyApp(App):
    def build(self):
        # Manejador de pantallas
        self.screen_manager = ScreenManager()
        
        # Pantallas
        self.input_screen = InputScreen(name="input")
        self.image_screen = ImageScreen(name="image")
        
        # Agregar pantallas al manejador de pantallas
        self.screen_manager.add_widget(self.input_screen)
        self.screen_manager.add_widget(self.image_screen)
        
        return self.screen_manager

if __name__ == "__main__":
    MyApp().run()