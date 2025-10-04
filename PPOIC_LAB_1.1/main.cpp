#include <SFML/Graphics.hpp>   // HUD/меню
#include <SFML/OpenGL.hpp>
#include "RubikCube.hpp"
#include "Menu.hpp"
#include <iostream>
#include <cstring>
#include <string>

static void setViewport(const sf::Window& w) {
    auto sz = w.getSize();
    glViewport(0, 0, static_cast<GLsizei>(sz.x), static_cast<GLsizei>(sz.y));
}

int main() {
    sf::ContextSettings settings;
    settings.depthBits = 24;
    settings.stencilBits = 8;
    settings.antialiasingLevel = 0;
    settings.majorVersion = 2; // fixed pipeline
    settings.minorVersion = 1;

    // Заголовок окна (UTF-8 -> sf::String)
    const std::u8string title8 =
        u8"Rubik’s Cube — U/D/L/R/F/B, Shift=CCW | Esc=Menu";
    sf::String title = sf::String::fromUtf8(
        reinterpret_cast<const char*>(title8.data()),
        reinterpret_cast<const char*>(title8.data() + title8.size())
    );

    // SFML RenderWindow для совместного рисования SFML + OpenGL
    sf::RenderWindow window(
        sf::VideoMode({900u, 700u}),
        title,
        sf::Style::Default,
        settings
    );
    window.setVerticalSyncEnabled(true);
    // window.setKeyRepeatEnabled(false); // если нужно, можно отключить автоповтор

    // OpenGL init
    glEnable(GL_DEPTH_TEST);
    glDepthFunc(GL_LESS);
    glDisable(GL_CULL_FACE);
    glClearColor(0.10f, 0.11f, 0.13f, 1.0f);

    setViewport(window);

    RubikCube cube;
    Menu menu;

    bool inMenu = true;   // стартуем в меню
    menu.init();
    menu.show();
    menu.onOpen();

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {

            if (event.type == sf::Event::Closed) {
                window.close();
                continue;
            }

            if (event.type == sf::Event::Resized) {
                setViewport(window);
                continue;
            }

            // ===== ГЛОБАЛЬНЫЙ ОБРАБОТЧИК ОТКРЫТИЯ МЕНЮ =====
            if (event.type == sf::Event::KeyPressed) {
                if ((event.key.code == sf::Keyboard::Escape ||
                     event.key.code == sf::Keyboard::M)      // альтернативный хоткей
                    && !inMenu) {
                    inMenu = true;
                    menu.onOpen();
                    std::cout << "\n[Открыто меню (Esc/M)]\n";
                    // Не даём событию дальше обрабатываться "игрой"
                    continue;
                }
            }
            // =================================================

            if (inMenu) {
                // Меню само выставит inMenu=false, когда нужно
                menu.handleEvent(event, window, cube, inMenu);
            } else {
                // Игра
                cube.handleEvent(event);
            }
        }

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        auto sz = window.getSize();
        cube.update();
        cube.render(static_cast<int>(sz.x), static_cast<int>(sz.y));

        // Оверлей меню поверх OpenGL
        if (inMenu) {
            window.pushGLStates();
            menu.draw(window);
            window.popGLStates();
        }

        window.display();
    }
    return 0;
}
