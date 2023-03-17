#include <LiquidCrystal.h>
#include <Keypad.h>
#include <ArduinoJson.h>

// Definimos los pines de la pantalla LCD
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

// Definimos los pines del teclado matricial
const byte ROWS = 4;
const byte COLS = 4;
char keys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};
byte rowPins[ROWS] = {9, 8, 7, 6};
byte colPins[COLS] = {13, 10, A3, A2};
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

// Definimos las opciones del menú
const int NUM_OPTIONS = 5;
const char* options[NUM_OPTIONS] = {
  "Sensores",
  "Actuadores",
  "Ajustes",
  "Otros",
  "Salir"
};
const int NUM_SUBOPTIONS = 5;
const char* suboptions[NUM_OPTIONS][NUM_SUBOPTIONS] = {
  {"Temperatura Interna", "Temperatura Externa", "Oxigeno", "pH", "Nivel de Agua"},
  {"Bomba de Agua", "Calentadores", "Aireadores", "", ""},
  {"Modo Seguro", "", "", "", ""},
  {"", "", "", "", ""},
  {"", "", "", "", ""}
};

// Definimos el índice de la opción seleccionada y el índice del submenú seleccionado
int selected_option = 0;
int selected_suboption = 0;

// Función para imprimir el menú en la pantalla LCD
void printMenu() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("> ");
  lcd.print(options[selected_option]);
  lcd.setCursor(0, 1);
  for (int i = 0; i < NUM_SUBOPTIONS; i++) {
    lcd.print(suboptions[selected_option][i]);
    lcd.print("   ");
  }
}

// Función para mover el selector hacia arriba
void moveSelectorUp() {
  if (selected_suboption > 0) {
    selected_suboption--;
  } else if (selected_option > 0) {
    selected_option--;
    selected_suboption = NUM_SUBOPTIONS - 1;
  }
}

// Función para mover el selector hacia abajo
void moveSelectorDown() {
  if (selected_suboption < NUM_SUBOPTIONS - 1 && suboptions[selected_option][selected_suboption + 1][0] != '\0') {
    selected_suboption++;
  } else if (selected_option < NUM_OPTIONS - 1) {
    selected_option++;
    selected_suboption = 0;
  }
}

// Función para procesar la selección
void processSelection() {
  if (selected_option == 3) {  // Si se selecciona la opción "Salir", salimos del programa
    exit(0);} else if (suboptions[selected_option][selected_suboption][0] != '\0') { // Si se selecciona una opción válida, imprimimos el submenú correspondiente
lcd.clear();
lcd.print(suboptions[selected_option][selected_suboption]);
}
}

void setup() {
Serial.begin(9600);
lcd.begin(20, 4);
}

void loop() {
// Actualizamos el menú en función del JSON recibido por el puerto serial
while (Serial.available()) {
String json = Serial.readStringUntil('\n');
StaticJsonDocument<256> doc;
DeserializationError error = deserializeJson(doc, json);
if (error) {
Serial.println("Error al deserializar JSON");
} else {
// Actualizamos las opciones del menú y del submenú en función del JSON
for (int i = 0; i < NUM_OPTIONS; i++) {
options[i] = doc["menu"][i]["name"];
for (int j = 0; j < NUM_SUBOPTIONS; j++) {
if (j < doc["menu"][i]["submenu"].size()) {
suboptions[i][j] = doc["menu"][i]["submenu"][j]["name"];
} else {
suboptions[i][j] = "";
}
}
}
// Imprimimos el menú actualizado
printMenu();
}
}

// Leemos las teclas del teclado matricial
char key = keypad.getKey();

// Procesamos la tecla presionada
if (key == 'A') { // Si se presiona la tecla "A", movemos el selector hacia arriba
moveSelectorUp();
printMenu();
} else if (key == 'B') { // Si se presiona la tecla "B", movemos el selector hacia abajo
moveSelectorDown();
printMenu();
} else if (key == 'C') { // Si se presiona la tecla "C", procesamos la selección
processSelection();
} else if (key == 'D') { // Si se presiona la tecla "D", regresamos al menú principal
selected_suboption = 0;
printMenu();
}
}

