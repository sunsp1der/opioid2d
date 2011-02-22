
#include "util.hpp"
#ifdef DARWIN
#include <gl.h>
#else
#include <GL/gl.h>
#endif

#include "scene.hpp"
#include "layer.hpp"
#include "sprite.hpp"
#include "debug.hpp"
#include "lighting.hpp"
#include "num.hpp"
#include "director.hpp"
#include "camera.hpp"
#include "display.hpp"

#include <cmath>
#include <iostream>

namespace opi2d
{
    Scene::Scene() : callbacks(NULL)
    {FUNC
        this->camera = new Camera();
    }
    
    Scene::~Scene()
    {FUNC
        for(Layers::iterator i=layers.begin();i != layers.end();++i)
        {
            delete (*i);
        }
        for(Lights::iterator i=lights.begin(); i != lights.end(); ++i)
        {
            (*i)->Delete();
        }
    }
    
    void Scene::SetCallbacks(SceneCallbacks* callback)
    {FUNC
        this->callbacks = callback;
    }
    
    SceneCallbacks* Scene::GetCallbacks()
    {FUNC
        return this->callbacks;
    }
    
    void Scene::AddLayer(const std::string& name)
    {FUNC
        Layer *l = new Layer(name);
        this->layers.push_back(l);
        this->namemap[name] = l;
    }
    
    void Scene::DeleteLayer(const std::string& name)
    {
    	this->DeleteLayer(this->GetLayer(name));
    }
    
    void Scene::DeleteLayer(Layer* layer)
    {
    	if (layer == NULL) return;
    	for (Layers::iterator i = layers.begin(); i != layers.end(); ++i)
    	{
    		if (*i == layer)
    		{
    			this->layers.erase(i);
    			break;
    		}
    	}
    	this->namemap.erase(layer->GetName());
    	delete layer;
    }
    
    Layers Scene::GetLayers()
    {
	    return this->layers;
    }

    void Scene::SetLayers( Layers layers)
    {
	    this->layers = layers;
    }

    void Scene::AddLight(Light* light)
    {
        this->lights.insert(light);
    }
    
    void Scene::RemoveLight(Light* light)
    {
        this->lights.erase(light);
    }
    
    void Scene::SetAmbientLight(const Color& color)
    {
        this->ambient_light = color;
    }
    
    void Scene::update_lights()
    {
        for(Lights::iterator i=lights.begin(); i != lights.end(); ++i)
        {
            Light* l = (*i);
            l->worldpos = l->pos;
            if (l->node != NULL)
            {
                const Mat9& mat = l->node->GetTransformationMatrix();
                mat.transform(l->worldpos);
            }
        }
    }    
    
    Color Scene::CalculateLight(const Vec2& pos)
    {
        Color color = this->ambient_light;
        for(Lights::iterator i=lights.begin(); i != lights.end(); ++i)
        {
            Light* l = (*i);
            Vec2& lpos = l->worldpos;
            floatval dx = fabs(lpos.x-pos.x);
            floatval dy = fabs(lpos.y-pos.y);
            floatval dist2 = dx*dx + dy*dy;
            if (dist2 >= l->cutoff*l->cutoff)
            {
                continue;
            }
            floatval in = l->intensity;
            if (dist2 <= in * in)
            {
                color += l->color;
            }
            else
            {
                floatval mult = (in*in)/dist2;
                color += l->color * mult;
            }
        }
        //color.trimvalues();
        color.alpha = 1.0f;
        /*std::cout << color.red << ' ';
        std::cout << color.green << ' ';
        std::cout << color.blue << ' ';
        std::cout << color.alpha << ' ';
        std::cout << std::endl;*/
        return color;
    }
    
    void Scene::RealTick()
    {
    }
    
    void Scene::Tick()
    {
    	this->manager.Iterate();
        for(SpriteGroups::iterator i=groups.begin(); i != groups.end(); ++i)
        {
            i->second->Tick();
        }
        for(Collisions::iterator i=collisions.begin(); i != collisions.end(); ++i)
        {
            const std::string& name1 = i->first;
            const std::string& name2 = i->second;
            SpriteGroup* group1 = GetGroup(name1);
            SpriteGroup* group2 = GetGroup(name2);
            if (group1 == NULL || group2 == NULL) continue;
            group1->Lock();
            for(SpriteSet::iterator sprite1=group1->Begin(); sprite1 != group1->End(); ++sprite1)
            {
                Sprite* spr1 = *sprite1;
                if (spr1->IsDeleted()) continue;
                spr1->TransformCollisionNodes();
                group2->Lock();
                for(SpriteSet::iterator sprite2=group2->Begin(); sprite2 != group2->End(); ++sprite2)
                {
                    Sprite* spr2 = *sprite2;
                    if (spr2->IsDeleted()) continue;
                    if (spr1 == spr2) continue;
                    spr2->TransformCollisionNodes();
                    CollisionNodes& nodes1 = spr1->collnodes;
                    CollisionNodes& nodes2 = spr2->collnodes;
                    for(CollisionNodes::iterator col1=nodes1.begin(); col1 != nodes1.end(); ++col1)
                    {                        
                        for(CollisionNodes::iterator col2=nodes2.begin(); col2 != nodes2.end(); ++col2)
                        {
                            if (col1->CheckOverlap(*col2))
                            {
                            	//std::cout << (int)spr1 << std::endl;
                            	//std::cout << name1 << ':' << name2 << std::endl;
                                this->callbacks->OnCollision(name1, name2, spr1, spr2);
                                // skip all the rest of the collision nodes if these sprites have
                                // several, so that no multiple collisions are registered for the
                                // same pair
                                goto skipnodes;
                            }
                        }
                    }
                    skipnodes:
                    ;
                }
                group2->Unlock();
            }
            group1->Unlock();
        }
    }
    
    void Scene::Render()
    {//FUNC
        const Vec2& units = Display::GetInstance()->GetViewSize();
        const int ux = (int)(units.x / 2);
        const int uy = (int)(units.y / 2);
        if (this->lights.size() > 0) this->update_lights();
        this->camera->Adjust();
        for(Layers::iterator i=this->layers.begin(); i != this->layers.end(); ++i)
        {
            Layer* layer = (*i);
            glPushMatrix();
            if (!layer->ignore_camera) {
		        Camera* c = this->camera;
	            Vec2 pos = c->GetPos();
	            pos *= layer->camera_offset;
	            glTranslatef(ux, uy, 0);
	            glRotatef(c->GetRotation() * layer->camera_rotation, 0,0,1);
	            const Vec2& scale = c->GetScale();
	            floatval x = layer->camera_zoom * (scale.x-1.0) + 1.0;
	            floatval y = layer->camera_zoom * (scale.y-1.0) + 1.0;
	            glScalef(x, y, 1);
	            glTranslatef(-pos.x, -pos.y, 0);
	            layer->Render();
	            glPopMatrix();
            }
            else
            {
            	layer->Render();
            }
        }
    }
    
    SpriteGroup* Scene::GetGroup(const std::string& name)
    {
        SpriteGroups::iterator i = groups.find(name);
        if (i == groups.end())
        {
            return NULL;
        }
        return i->second;
    }
    
    SpriteGroup* Scene::CreateGroup(const std::string& name)
    {
        SpriteGroup* group = GetGroup(name);
        if (group == NULL)
        {
            group = new SpriteGroup(name);
            groups[name] = group;
        }
        return group;
    }
    
    void Scene::EnableCollisions(const std::string& group1, const std::string& group2)
    {
        this->collisions.insert(NamePair(group1, group2));
    }
    
    void Scene::DisableAllCollisions()
    {
    	this->collisions.clear();
    }
    
    void Scene::AddAction(Action* action)
    {
    	this->manager.AddAction(action);
    }
    
    void Scene::RemoveAction(Action* action)
    {
    	this->manager.RemoveAction(action);
    }
}
