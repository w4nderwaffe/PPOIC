#include "Menu.hpp"
#include <iostream>
#include <filesystem>

// ---------- приватные утилиты: шрифт ----------

bool Menu::tryLoadFont(const std::string& path) {
    std::error_code ec;
    if (std::filesystem::exists(path, ec)) {
        if (font_.loadFromFile(path)) {
            loadedFontPath_ = path;
            return true;
        }
    }
    return false;
}

void Menu::loadFirstAvailableFont() {
    // 1) Проектный ассет
    if (tryLoadFont("assets/DejaVuSans.ttf")) { fontLoaded_ = true; return; }
    if (tryLoadFont("assets/DejaVuSansMono.ttf")) { fontLoaded_ = true; return; }

    // 2) Популярные системные пути (macOS / Linux / Windows)
#if defined(__APPLE__)
    if (tryLoadFont("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")) { fontLoaded_ = true; return; }
    if (tryLoadFont("/System/Library/Fonts/Supplemental/Arial Unicode MS.ttf")) { fontLoaded_ = true; return; }
    if (tryLoadFont("/Library/Fonts/Arial Unicode.ttf")) { fontLoaded_ = true; return; }
#elif defined(_WIN32)
    {
        const char* windir = std::getenv("WINDIR");
        std::string base = windir ? windir : "C:\\Windows";
        if (tryLoadFont(base + "\\Fonts\\arialuni.ttf")) { fontLoaded_ = true; return; }
        if (tryLoadFont(base + "\\Fonts\\segoeui.ttf"))  { fontLoaded_ = true; return; }
    }
#else
    if (tryLoadFont("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")) { fontLoaded_ = true; return; }
    if (tryLoadFont("/usr/share/fonts/truetype/freefont/FreeSans.ttf")) { fontLoaded_ = true; return; }
#endif

    fontLoaded_ = false;
}

// ---------- публичное ----------

void Menu::init() {
    loadFirstAvailableFont();
    if (!fontLoaded_) {
        std::cerr << "[Menu] ВНИМАНИЕ: не удалось загрузить шрифт."
                     " Положи TTF, напр., assets/DejaVuSans.ttf\n";
    } else {
        std::cout << "[Menu] Шрифт: " << loadedFontPath_ << "\n";
    }

    // даже если шрифт не загружен, тексты инициализируем — просто их не нарисуем
    titleText_.setFont(font_);
    hintText_.setFont(font_);
    titleText_.setCharacterSize(theme_.titleSize);
    hintText_.setCharacterSize(theme_.hintSize);
    titleText_.setFillColor(theme_.textColor);
    hintText_.setFillColor(sf::Color(200,200,205));

    // строки в UTF-8 -> sf::String
    {
        const std::string titleUtf8 = "М Е Н Ю";
        titleText_.setString(sf::String::fromUtf8(titleUtf8.begin(), titleUtf8.end()));
        const std::string hintUtf8  = "1–5 или клик мышью • 0 / Esc — вернуться в игру";
        hintText_.setString(sf::String::fromUtf8(hintUtf8.begin(), hintUtf8.end()));
    }

    ensureItems();
}

void Menu::onOpen() {
    hovered_ = -1;
}

void Menu::show() {
    std::cout <<
        "\n======= М Е Н Ю =======\n"
        "  1 — Начать с СОБРАННОГО куба\n"
        "  2 — Начать с РАЗОБРАННОГО (скрамбл)\n"
        "  3 — Загрузить из файла (cube.txt)\n"
        "  4 — Сохранить текущее состояние (cube.txt)\n"
        "  5 — Выход из игры\n"
        "  0 / Esc — Вернуться в игру (без изменений)\n"
        "=======================\n"
        "Сделайте выбор: ";
    std::cout.flush();
}

void Menu::draw(sf::RenderWindow& window) {
    sf::FloatRect panel;
    std::vector<sf::FloatRect> itemRects;
    sf::Vector2f titlePos, hintPos;
    
    // ИСПРАВЛЕНО: computeLayout вместо computeLayout_
    computeLayout(window, panel, itemRects, titlePos, hintPos);
    itemRects_ = itemRects;

    // 1) Оверлей
    sf::RectangleShape overlay({(float)window.getSize().x, (float)window.getSize().y});
    overlay.setFillColor(theme_.overlayColor);
    window.draw(overlay);

    // 2) Панель
    sf::RectangleShape panelShape({panel.width, panel.height});
    panelShape.setPosition(panel.left, panel.top);
    panelShape.setFillColor(theme_.panelColor);
    panelShape.setOutlineThickness(1.f);
    panelShape.setOutlineColor(theme_.borderColor);
    window.draw(panelShape);

    // 3) Заголовок и подсказка — рисуем только если шрифт загружен
    if (fontLoaded_) {
        titleText_.setPosition(titlePos);
        window.draw(titleText_);
    }

    // 4) Элементы
    for (std::size_t i = 0; i < items_.size(); ++i) {
        const auto& r = itemRects[i];

        // фон кнопки
        sf::RectangleShape btn({r.width, r.height});
        btn.setPosition(r.left, r.top);
        btn.setFillColor((int)i == hovered_ ? theme_.itemBgHover : theme_.itemBg);
        btn.setOutlineThickness(1.f);
        btn.setOutlineColor(theme_.borderColor);
        window.draw(btn);

        // текст — только если есть шрифт
        if (fontLoaded_) {
            sf::Text txt;
            txt.setFont(font_);
            txt.setCharacterSize(theme_.itemSize);
            txt.setFillColor((int)i == hovered_ ? theme_.hotTextColor : theme_.textColor);

            const auto& s = items_[i].labelUtf8; // std::string (UTF-8)
            txt.setString(sf::String::fromUtf8(s.begin(), s.end()));

            const float padX = 16.f;
            const float padY = (r.height - txt.getLocalBounds().height) * 0.5f - txt.getLocalBounds().top;
            txt.setPosition(r.left + padX, r.top + padY);
            window.draw(txt);
        }
    }

    if (fontLoaded_) {
        hintText_.setPosition(hintPos);
        window.draw(hintText_);
    }
}

void Menu::handleEvent(const sf::Event& e, sf::RenderWindow& window, RubikCube& cube, bool& inMenu) {
    if (e.type == sf::Event::MouseMoved) {
        sf::Vector2f p((float)e.mouseMove.x, (float)e.mouseMove.y);
        hovered_ = -1;
        for (int i = 0; i < (int)itemRects_.size(); ++i) {
            if (itemRects_[i].contains(p)) { hovered_ = i; break; }
        }
    }

    if (e.type == sf::Event::MouseButtonPressed && e.mouseButton.button == sf::Mouse::Left) {
        sf::Vector2f p((float)e.mouseButton.x, (float)e.mouseButton.y);
        for (int i = 0; i < (int)itemRects_.size(); ++i) {
            if (itemRects_[i].contains(p)) {
                // ИСПРАВЛЕНО: doAction вместо doAction_
                doAction(i, window, cube, inMenu);
                return;
            }
        }
    }

    if (e.type == sf::Event::KeyPressed) {
        // Esc / 0 — выйти из меню без изменений
        if (e.key.code == sf::Keyboard::Escape ||
            e.key.code == sf::Keyboard::Num0 ||
            e.key.code == sf::Keyboard::Numpad0) {
            inMenu = false;
            std::cout << "\n[Меню закрыто]\n";
            return;
        }

        // Соответствие пунктам
        for (int i = 0; i < (int)items_.size(); ++i) {
            for (auto k : items_[i].keys) {
                if (e.key.code == k) {
                    // ИСПРАВЛЕНО: doAction вместо doAction_
                    doAction(i, window, cube, inMenu);
                    return;
                }
            }
        }

        if (e.key.code == sf::Keyboard::Enter || e.key.code == sf::Keyboard::Return) show();
    }
}

// ---------- приватное ----------

void Menu::ensureItems() {
    if (!items_.empty()) return;
    items_ = {
        ItemDesc{ "1 — Начать с СОБРАННОГО куба",
            { sf::Keyboard::Num1, sf::Keyboard::Numpad1 } },
        ItemDesc{ "2 — Начать с РАЗОБРАННОГО (скрамбл 25 ходов)",
            { sf::Keyboard::Num2, sf::Keyboard::Numpad2, sf::Keyboard::R } },
        ItemDesc{ "3 — Загрузить из файла (cube.txt)",
            { sf::Keyboard::Num3, sf::Keyboard::Numpad3, sf::Keyboard::L } },
        ItemDesc{ "4 — Сохранить текущее состояние (cube.txt)",
            { sf::Keyboard::Num4, sf::Keyboard::Numpad4, sf::Keyboard::S } },
        ItemDesc{ "5 — Выход из игры",
            { sf::Keyboard::Num5, sf::Keyboard::Numpad5, sf::Keyboard::Q } },
    };
}

void Menu::doAction(int index, sf::RenderWindow& window, RubikCube& cube, bool& inMenu) {
    switch (index) {
        case 0:
            cube.initSolved();
            std::cout << "\n— Старт: СОБРАННЫЙ куб.\n";
            inMenu = false;
            std::cout << "\n[Меню закрыто]\n";
            break;
        case 1:
            cube.initRandom(25);
            std::cout << "\n— Старт: РАЗОБРАННЫЙ (скрамбл 25 ходов).\n";
            inMenu = false;
            std::cout << "\n[Меню закрыто]\n";
            break;
        case 2: {
            const std::string path = "cube.txt";
            if (cube.loadFromFile(path)) {
                std::cout << "\n— Загрузили состояние из " << path << ".\n";
                inMenu = false;
                std::cout << "\n[Меню закрыто]\n";
            } else {
                std::cout << "\n! Ошибка загрузки из " << path << ". Останемся в меню.\n";
                std::cout.flush();
            }
            break;
        }
        case 3: {
            const std::string path = "cube.txt";
            if (cube.saveToFile(path)) {
                std::cout << "\n— Сохранили состояние в " << path << ".\n";
            } else {
                std::cout << "\n! Не удалось сохранить в " << path << ". Проверь права/путь.\n";
            }
            // остаёмся в меню
            break;
        }
        case 4:
            std::cout << "\n— Выход.\n";
            window.close();
            break;
        default: break;
    }
}

void Menu::computeLayout(sf::RenderWindow& window,
                          sf::FloatRect& panelRect,
                          std::vector<sf::FloatRect>& itemRects,
                          sf::Vector2f& titlePos,
                          sf::Vector2f& hintPos) {
    const float W = (float)window.getSize().x;
    const float H = (float)window.getSize().y;

    const int itemCount = (int)items_.size();
    const float panelW = theme_.panelWidth;
    const float titleH = (float)theme_.titleSize + 8.f;
    const float hintH  = (float)theme_.hintSize + 6.f;
    const float itemsH = itemCount * theme_.itemHeight + (itemCount - 1) * theme_.itemGap;
    const float panelH = theme_.panelPadding + titleH + 16.f + itemsH + 20.f + hintH + theme_.panelPadding;

    const float panelX = std::floor((W - panelW) * 0.5f);
    const float panelY = std::floor((H - panelH) * 0.5f);

    panelRect = { panelX, panelY, panelW, panelH };

    titlePos = { panelX + theme_.panelPadding, panelY + theme_.panelPadding };

    itemRects.clear();
    float curY = titlePos.y + titleH + 16.f;
    const float itemX = panelX + theme_.panelPadding;
    const float itemW = panelW - 2.f * theme_.panelPadding;

    for (int i = 0; i < itemCount; ++i) {
        itemRects.emplace_back(itemX, curY, itemW, theme_.itemHeight);
        curY += theme_.itemHeight + theme_.itemGap;
    }

    hintPos = { panelX + theme_.panelPadding, panelY + panelH - theme_.panelPadding - hintH + 6.f };
}
