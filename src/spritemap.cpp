
#include "spritemap.hpp"
#include "sprite.hpp"

namespace opi2d
{
	void SpriteMapper::AddSprite(const std::string& type, Sprite* sprite)
	{
		this->sprites[sprite->GetID()] = type;
	}
	
	const std::string SpriteMapper::RemoveSprite(Sprite* sprite)
	{
		IdMap::iterator i = this->sprites.find(sprite->GetID());
		if (i == this->sprites.end()) return "";
		return i->second;
	} 
}
