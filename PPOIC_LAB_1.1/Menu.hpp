#pragma once
#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include "RubikCube.hpp"
#include <string>
#include <vector>
#include <functional>

#ifdef TESTING
#define TESTABLE public
#else
#define TESTABLE private
#endif

class Menu {
public:
    // Инициализация ресурсов (шрифт/стили)
    void init();

    // Вызывается при входе в меню (сброс наведений)
    void onOpen();

    // Печать меню в консоль (опционально)
    void show();

    // Отрисовка оверлея меню поверх OpenGL
    void draw(sf::RenderWindow& window);

    // Обработка событий. Меняет cube/window/inMenu согласно выбору
    void handleEvent(const sf::Event& e, sf::RenderWindow& window, RubikCube& cube, bool& inMenu);

// Методы для тестирования
TESTABLE:
    void ensureItems();
    void doAction(int index, sf::RenderWindow& window, RubikCube& cube, bool& inMenu);
    void computeLayout(sf::RenderWindow& window,
                      sf::FloatRect& panelRect,
                      std::vector<sf::FloatRect>& itemRects,
                      sf::Vector2f& titlePos,
                      sf::Vector2f& hintPos);
    bool tryLoadFont(const std::string& path);
    void loadFirstAvailableFont();

// Приватные поля (не для тестирования)
private:
    sf::Font font_;
    bool fontLoaded_ = false;
    std::string loadedFontPath_;
    sf::Text titleText_;
    sf::Text hintText_;
    std::vector<sf::FloatRect> itemRects_;
    int hovered_ = -1;
    
    struct Theme {
        float panelWidth = 560.f;
        float itemHeight = 48.f;
        float itemGap    = 14.f;
        float panelPadding = 24.f;
        unsigned titleSize = 28;
        unsigned itemSize  = 22;
        unsigned hintSize  = 18;
        sf::Color overlayColor = sf::Color(10,10,12,180);
        sf::Color panelColor   = sf::Color(24,26,30,240);
        sf::Color borderColor  = sf::Color(80,90,110,220);
        sf::Color textColor    = sf::Color(230,232,236);
        sf::Color hotTextColor = sf::Color(255,255,255);
        sf::Color itemBg       = sf::Color(40,44,52,220);
        sf::Color itemBgHover  = sf::Color(70,76,90,240);
    } theme_;
    
    struct ItemDesc {
        std::string labelUtf8;
        std::vector<sf::Keyboard::Key> keys;
    };
    std::vector<ItemDesc> items_;
};
