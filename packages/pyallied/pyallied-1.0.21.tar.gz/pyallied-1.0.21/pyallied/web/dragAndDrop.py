import os

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seletools.actions import drag_and_drop

from pyallied.web.webWaits import customwebDriverwait


class DragAndDrop(customwebDriverwait):
    # drag and drop
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        '''
        drag_and_drop(source, target)¶
        Holds down the left mouse button on the source element,
        then moves to the target element and releases the mouse button.
        Args:	
        source: The element to mouse down.
        target: The element to mouse up
        '''

    def dragAndDrop(self, sourcexpath, destinationxpath):
        try:
            SourceelElementPresense = super().WaitFor_PresenseOf_Element_Located(sourcexpath)
            SourceelElementVisibility = super().WaitFor_VisibilityOf_Element_Located(sourcexpath)
            DestinationElementPresense = super().WaitFor_PresenseOf_Element_Located(destinationxpath)
            DestinationElementVisibility = super().WaitFor_VisibilityOf_Element_Located(destinationxpath)
            if SourceelElementPresense:
                if DestinationElementPresense:
                    if SourceelElementVisibility:
                        if DestinationElementVisibility:
                            sourceElement = self.driver.find_element(By.XPATH, sourcexpath)
                            destination = self.driver.find_element(By.XPATH, destinationxpath)
                            action_chains = ActionChains(self.driver)
                            action_chains.drag_and_drop(sourceElement, destination).perform()

                        else:
                            self.__raise_element_not_visible_exception(destinationxpath)
                    else:
                        self.__raise_element_not_visible_exception(sourcexpath)
                else:
                    self.__raise_element_not_present_exception(destinationxpath)
            else:
                self.__raise_element_not_present_exception(sourcexpath)
        except Exception as error:
            raise error
        '''
        drag_and_drop_by_offset(source, xoffset, yoffset)¶
        Holds down the left mouse button on the source element,
        then moves to the target offset and releases the mouse button.
        Args:	
        source: The element to mouse down.
        xoffset: X offset to move to.
        yoffset: Y offset to move to.
        '''

    def dragAndDropByOffset(self, sourcexpath, xoffset, yoffset):
        try:
            SourceelElementPresense = super().WaitFor_PresenseOf_Element_Located(sourcexpath)
            SourceelElementVisibility = super().WaitFor_VisibilityOf_Element_Located(sourcexpath)
            if (SourceelElementPresense):
                if (SourceelElementVisibility):
                    action_chains = ActionChains(self.driver)
                    action_chains.drag_and_drop_by_offset(
                        SourceelElementVisibility, xoffset, yoffset).pause(5).perform()
                else:
                    self.__raise_element_not_visible_exception(sourcexpath)
            else:
                self.__raise_element_not_present_exception(sourcexpath)
        except Exception as error:
            raise error

    def dragElement_ToOffSet_And_Drop(self, sourcexpath, xoffset, yoffset):
        try:
            SourceelElementPresense = super().WaitFor_PresenseOf_Element_Located(sourcexpath)
            SourceelElementVisibility = super().WaitFor_VisibilityOf_Element_Located(sourcexpath)
            if (SourceelElementPresense):
                if (SourceelElementVisibility):
                    action_chains = ActionChains(self.driver)

                    action_chains.move_to_element(SourceelElementVisibility).pause(1).click_and_hold().pause(
                        2).move_by_offset(xoffset, yoffset).pause(2).release().perform()
                else:
                    self.__raise_element_not_visible_exception(sourcexpath)
            else:
                self.__raise_element_not_present_exception(sourcexpath)
        except Exception as error:
            raise error

    def seletools_drag_and_drop_xpath(self, sourcexpath, destinationxpath):
        try:
            SourceelElementPresense = super().WaitFor_PresenseOf_Element_Located(sourcexpath)
            SourceelElementVisibility = super().WaitFor_VisibilityOf_Element_Located(sourcexpath)
            DestinationElementPresense = super().WaitFor_PresenseOf_Element_Located(destinationxpath)
            DestinationElementVisibility = super().WaitFor_VisibilityOf_Element_Located(destinationxpath)
            if (SourceelElementPresense):
                if DestinationElementPresense:
                    if SourceelElementVisibility:
                        if DestinationElementVisibility:
                            drag_and_drop(self.driver, SourceelElementVisibility, DestinationElementVisibility)
                        else:
                            self.__raise_element_not_visible_exception(destinationxpath)
                    else:
                        self.__raise_element_not_visible_exception(sourcexpath)
                else:
                    self.__raise_element_not_present_exception(destinationxpath)
            else:
                self.__raise_element_not_present_exception(sourcexpath)


        except Exception as error:
            raise error

    def seletools_drag_and_drop_css(self, source_css, destination_css):
        try:
            SourceelElementPresense = self.__waitFor_presenseOf_element_located(source_css)
            SourceelElementVisibility = self.__waitFor_visibilityOf_element_located(source_css)
            DestinationElementPresense = self.__waitFor_presenseOf_element_located(destination_css)
            DestinationElementVisibility = self.__waitFor_visibilityOf_element_located(destination_css)
            if (SourceelElementPresense):
                if DestinationElementPresense:
                    if SourceelElementVisibility:
                        if DestinationElementVisibility:
                            drag_and_drop(self.driver, SourceelElementVisibility, DestinationElementVisibility)
                        else:
                            self.__raise_element_not_visible_exception(destination_css)
                    else:
                        self.__raise_element_not_visible_exception(source_css)
                else:
                    self.__raise_element_not_present_exception(destination_css)
            else:
                self.__raise_element_not_present_exception(source_css)
        except Exception as error:
            raise error

    '''
    ATTENTION: you must use CSS selectors for draggable and droppable elements in order for this script to work. 
    It’s related to the way that browser search elements in DOM tree using embedded scripts
    '''

    def dragAndDrop_cssSelectorOnly_jsExecuter(self, source_css, destination_css):
        try:
            # file_path=os.path.dirname(__file__)
            f = open(os.path.dirname(__file__) + "\dragDrop.js", "r")
            javascript = f.read()
            f.close()
            self.driver.execute_script(javascript, source_css, destination_css)
        except Exception as error:
            raise error

    def moveToElement_WithOffset_and_drag_and_drop(self, xpath, xoffset_click, yoffset_click, xoffset_move,
                                                   yoffset_move):
        try:
            actions = ActionChains(self.driver)
            elementPresense = super().WaitFor_PresenseOf_Element_Located(xpath)
            elementVisible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if elementPresense:
                if elementVisible:
                    # element = self.driver.find_element(By.XPATH, xpath)
                    actions.move_to_element_with_offset(elementVisible, xoffset_click,
                                                        yoffset_click).click_and_hold().move_by_offset(xoffset_move,
                                                                                                       yoffset_move).release().pause(
                        1).perform()
                    # actions.perform()
                else:
                    self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def drag_and_drop_with_move_to_element(self, xpath_source, xpath_destination):
        try:
            actions = ActionChains(self.driver)
            elementPresense_source = super().WaitFor_PresenseOf_Element_Located(xpath_source)
            elementVisible_source = super().WaitFor_VisibilityOf_Element_Located(xpath_source)
            elementPresense_destination = super().WaitFor_PresenseOf_Element_Located(xpath_destination)
            elementVisible_destination = super().WaitFor_VisibilityOf_Element_Located(xpath_destination)
            if elementPresense_source:
                if elementVisible_source:
                    if elementPresense_destination:
                        if elementVisible_destination:

                            # element = self.driver.find_element(By.XPATH, xpath)
                            # actions.move_to_element_with_offset(elementVisible, xoffset, yoffset).click_and_hold().move_by_offset(xoffset_move,yoffset_move).release().pause(1).perform()
                            actions.move_to_element(elementVisible_source).click_and_hold().move_to_element(
                                elementVisible_destination).click().release().pause(1).perform()
                        # actions.perform()
                        else:
                            self.__raise_element_not_visible_exception(xpath_destination)
                    else:
                        self.__raise_element_not_present_exception(xpath_destination)
                else:
                    self.__raise_element_not_visible_exception(xpath_source)
            else:
                self.__raise_element_not_present_exception(xpath_source)
        except Exception as error:
            raise error

    def __waitFor_presenseOf_element_located(self, cssLocator):
        try:
            return WebDriverWait(self.driver, self.customWait).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, cssLocator)))
        except Exception as error:
            raise error

    def __waitFor_visibilityOf_element_located(self, cssLocator):
        try:
            # print(self.customWait,'------>wait')
            return WebDriverWait(self.driver, self.customWait).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, cssLocator)))
        except Exception as error:
            raise error

    def __raise_element_not_present_exception(self, locator):
        raise Exception("element not present : " + locator)

    def __raise_element_not_visible_exception(self, locator):
        raise Exception("element not visible : " + locator)
