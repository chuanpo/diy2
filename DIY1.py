import traceback

class DIY2:
    setting = {
        "标题" : "新版剧情",
        "说明" : "一键完成新版主线剧情。自动领取剧情完成奖励，自动完成所有新版剧情任务。",
        "类别" : "日常"
    }
    advXmlInfo = list()

    async def run(self, data, s):
        try:
            s.msgOut("{}-开始".format(self.setting["标题"]))
            
            self.advXmlInfo = s.configHelper.getFile("AdventureChapter.json")["AdventureChapter"]["Chapter"]
            await self.doChapter(s)

            s.msgOut("{}-结束".format(self.setting["标题"]))
        except Exception as e:
            s.msgOut(f"{traceback.format_exception(e)}")

    async def doChapter(self, s):
        for chapter in self.advXmlInfo:
            cId = chapter["ID"]
            cRId = chapter["ChapterRewardFlagID"]
            sRId = chapter["StoryRewardFlagID"]
            cInfo = chapter["ChapterRewardInfo"]["PassChapterReward"]
            sInfo = chapter["StoryRewardInfo"]["PassStoryReward"]
            
            va = await s.getMultiForever([sRId, cRId])
            curProgress = await self.doStory(s, cId, sInfo, va)

            for i in range(1, len(cInfo) + 1):
                if KTool.getBit(va[1], i) == 0 and curProgress >= cInfo[i - 1]["NeedPassStoryNum"]:
                    await s.sendInt("A1D6", [cId, i])
                    s.msgOut("{}-章节奖励{}-{}领取完毕".format(self.setting["标题"], cId, i))
                    va = await s.getMultiForever([sRId, cRId])
    
    async def doStory(self, s, cId, sInfo, va):
        curProgress = 0
        
        for sDict in sInfo:
            if not 'isFuture' in sDict:
                if not KTool.getBit(va[0], curProgress + 1):
                    await s.sendInt("A1D7", [cId, sDict["ID"]])
                    s.msgOut("{}-章节{}-{}完成".format(self.setting["标题"], cId, sDict["ID"]))
                curProgress += 1
        
        return curProgress

class KTool:
    @staticmethod
    def getBit(param1: int, param2: int) -> int:
        return param1 >> param2 - 1 & 1
