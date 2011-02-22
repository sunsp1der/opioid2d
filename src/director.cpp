
#include "director.hpp"
#include "display.hpp"
#include "scene.hpp"
#include "debug.hpp"
#include "actions.hpp"

namespace opi2d
{

    Director::Director() : quit(false), scene(NULL), tickid(0)
    {FUNC        
    }
   
    Director::~Director()
    {FUNC
    }
      
    void Director::Start(int now)
    {FUNC
        this->ticker.Start(now);
    }
   
       
    void Director::SetScene(Scene* scene)
    {FUNC
        this->scene = scene;
        DEBUG("SetScene END");
    }
   
    
    void Director::Iterate(int now)
    {FUNC
        ++tickid;
        this->ticker.Tick(now);
    }
    
    void Director::RenderFrame()
    {FUNC
        Display* display = Display::GetInstance();
        display->Clear();
        if (this->scene != NULL)
        {
            this->scene->Render();
        }
    }
   
   
}
