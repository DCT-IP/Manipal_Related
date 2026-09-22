#include <iostream>
#include <optional>
#include <SFML/Graphics.hpp>

int main(){
    std::cout << "Before Opening" << std::endl;
    sf::RenderWindow window(sf::VideoMode({800, 600}), "EcoSystemSim");
    sf::Vertex vertex;
    vertex.position = sf::Vector2f(10.f,50.f);
    vertex.color = sf::Color::Red;
    vertex.texCoords = sf::Vector2f(100.f,100.f);
    sf::VertexArray Tri(sf::PrimitiveType::Triangles, 3);
    Tri[0].position = sf::Vector2f(10.f, 10.f);
    Tri[1].position = sf::Vector2f(100.f,100.f);
    Tri[2].position = sf::Vector2f(100.f, 10.f);
    Tri[0].color = sf::Color::Red;
    Tri[1].color = sf::Color::Green;
    Tri[2].color = sf::Color::Blue;
    while(window.isOpen()){
        sf::Event event;
        while(window.pollEvent(event)){
            if (event.type == sf::Event::Closed)
                window.close();
        }
        window.clear(sf::Color::Black);
        window.draw(Tri);
        window.display();
    }
    std::cout << "After Opening " << std::endl;
    return 0;
}