#include <iostream>
#include <utility>
#include <SFML/Graphics.hpp>
int main() {
    std::pair<int, int> pos{0, 0};
    std::cout << "Before Opening\n"
              << "The coords are: "
              << pos.first << "," << pos.second << '\n';
    sf::RenderWindow window(
        sf::VideoMode({800, 600}),
        "EcoSystemSim"
    );
    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
            }
            if (event.type == sf::Event::KeyPressed) {
                if (event.key.scancode == sf::Keyboard::Scan::Escape) {
                    window.close();
                }
                if (event.key.scancode == sf::Keyboard::Scan::Space) {
                    std::cout << "Space pressed!\n";
                }
            }
        }
        if (sf::Keyboard::isKeyPressed(sf::Keyboard::W)) {
            pos.second -= 1;  
        }
        if (sf::Keyboard::isKeyPressed(sf::Keyboard::S)) {
            pos.second += 1;  
        }
        if (sf::Keyboard::isKeyPressed(sf::Keyboard::A)) {
            pos.first -= 1;   
        }
        if (sf::Keyboard::isKeyPressed(sf::Keyboard::D)) {
            pos.first += 1;   
        }
        window.clear(sf::Color::Black);
        window.display();
    }
    std::cout << "After Opening\n"
              << "The coords are: "
              << pos.first << "," << pos.second << '\n';
    return 0;
}
