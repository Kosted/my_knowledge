import requests
from bs4 import BeautifulSoup, SoupStrainer


s = requests.Session()
s.headers.update({
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
})

urlPattern = "https://www.kubsu.ru/"
url = urlPattern + 'ru/fktipm'
# url = urlPattern + 'ru/law'


# получение страницы с кафедрами
data = s.get(url).text

soup = BeautifulSoup(data, features="html.parser")

blockWithStructure = soup.find('div', {'id': 'field-faculty-structure'})


departmentList = blockWithStructure.findAll("ul")[0].findAll('a', href=True)


class Department:
    def __init__(self):
        self.lectors = list()

    def addLector(self, lector):
        self.lectors.append(lector)

    def getLectorNames(self):
        return [lector.name for lector in self.lectors]

    def getLector(self, name):
        for lector in self.lectors:
            if lector.name ==name:
                return lector


departments = list()


for departmentInfo in departmentList:
    tempDep = Department()
    tempDep.name = departmentInfo.getText()
    tempDep.link = departmentInfo['href']
    departments.append(tempDep)


class Lector:
    def __init__(self, name):
        self.name = name
        self.info = {}


for dep in departments:
    # поиск имен преподавателей
    print(urlPattern + dep.link)
    departmentsPage = s.get(urlPattern + dep.link).text

    departmentsPage = BeautifulSoup(departmentsPage, features="html.parser")

    #берем нижний блок содержащий всех преподавателей
    lectorBlock = departmentsPage.find("div", {"class": "views-responsive-grid views-responsive-grid-horizontal views-columns-6 img-maxwidth text-center font-12"})

    # в нем находим все имена
    lectorBlocks = lectorBlock.findAll("div", {"views-field views-field-field-employee-name"})


    # добавляем их в кафедру
    for lector in lectorBlocks:
        # print(lector.getText())
        dep.addLector(Lector(lector.getText().strip()))

    # поиск информации о преподователях
    allInfoBlock = departmentsPage.find("div", {"class": "field field-name-body field-type-text-with-summary field-label-hidden"}).findAll("p")
    # print(len(allInfoBlock))

    # ищем параграф с надписью преподаватели, удаляя все предыдущие параграфы
    p = allInfoBlock[0]
    while p.find("strong", string='Преподаватели') is None:
        allInfoBlock.pop(0)
        p = allInfoBlock[0]
    else:
        allInfoBlock.pop(0)

    lectorNameList = dep.getLectorNames()

    # выбор описания текущего преподавателя
    for p in allInfoBlock:
        # print(p.getText())
        # определение о ком данный блок
        if p.find("strong") is not None:
            strong = p.find("strong").getText()
            # print("strong = " + strong)
            for lector in lectorNameList:
                if lector in strong:
                    currentLector = dep.getLector(lector)
                    currentLector.info["primeryInfo"] = p.getText()
                    countInfo = 0
            if(countInfo !=0):
                currentLector.info[countInfo] = p.getText()
                countInfo += 1
        else:
            currentLector.info[countInfo] = p.getText()
            countInfo += 1
    #
    # обработать всего один факультет
    break

# декоратор
def border(*args, letter="*"):
    borderLenth = 100
    print(letter * borderLenth)
    if len(args) !=0:
        print(*args)
        print(letter * borderLenth)

printFullInfomation = True
printFullInfomation = False

# вывод в консоль
for dep in departments:
    border(dep.name, letter="=")

    for lector in dep.lectors:
        border(lector.name, letter="-",)
        if printFullInfomation:
            for info in lector.info.values():
                print(info)
            print("\n")
        else:
            if "primeryInfo" in lector.info:
                print(lector.info["primeryInfo"] + "\n")
        # border()
        # break
    # break























