import math
import random
import traceback

from time import time, sleep, strftime

# from org.sikuli.script.natives import Vision

# Sikuli Settings
Settings.MoveMouseDelay = 0.01


# Vision.setParameter("MinTargetSize", 8)


class Images(object):
    # Images and patterns
    SEARCH_TIMER = Pattern("searching.png").similar(0.98)
    SEARCH = Pattern("search.png").similar(0.96)
    NOTHING_WAS_FOUND = Pattern("HmeroHeHaneH.png").similar(0.91)
    OK = Pattern("ok-1.png").similar(0.80)
    MAIN_WINDOW = Pattern("1387646093669.png").similar(0.93)

    # OAKES
    OAK_IN_5_STEPS = ""
    OAK_IN_FRONT = Pattern("1399797623467.png").similar(0.71)
    OAK_ON_LEFT = Pattern("1399797814160.png").similar(0.71)
    OAK_ON_RIGHT = Pattern("1399798089279.png").similar(0.71)

    OAK_TREE = Pattern("1399800567248.png").similar(0.95)
    OAK_TREE2 = Pattern("1399800631560.png").similar(0.94)
    OAK_TREE3 = Pattern("1399800657439.png").similar(0.94)

    # PINES
    PINE_IN_5_STEPS = Pattern("1387714750295.png").similar(0.42)
    PINE_IN_FRONT = Pattern("COCHanpMOnep.png").similar(0.89)
    PINE_ON_LEFT = Pattern("1391623582480.png").similar(0.78)
    PINE_ON_RIGHT = Pattern("1391623760333.png").similar(0.75)

    PINE_TREE = Pattern("1391860017664.png").similar(0.90)
    PINE_TREE2 = Pattern("1391859761283.png").similar(0.85)
    PINE_TREE3 = Pattern("1391859902379.png").similar(0.85)

    NEED_AN_AXE = Pattern("1391335212591.png").similar(0.93)
    CRAFT_TIMER = Pattern("1387715184524.png").similar(0.98)
    CRAFT = Pattern("1387715339871.png").similar(0.96)

    MY_GROUP = False  # TODO: Add image with username
    WALK = Pattern("1390136065333.png").similar(0.89)

    ARROW = Pattern("1390247010387.png").similar(0.92)

    N = "1390142208550.png"
    S = "1390144256662.png"
    NE = "1390144318608.png"
    SE = "1390144334702.png"
    NW = "1390144358230.png"
    SW = "1390144374870.png"

    NW_POINT = Pattern("1390144834918.png").similar(0.91)
    NE_POINT = Pattern("1390144864670.png").similar(0.90)
    SW_POINT = Pattern("1390144910454.png").similar(0.90)
    SE_POINT = Pattern("1390144940646.png").similar(0.80)
    ROAD_PAVEMENT = Pattern("1390939645513.png").similar(0.86)
    AXE = Pattern("1391327999943.png").similar(0.95)
    BACKPACK = Pattern("1391328559159.png").similar(0.90)
    BP_TOOLS = Pattern("1391328620252.png").similar(0.97)
    BP_PUT = Pattern("1391328736039.png").similar(0.94)
    TRANSPARENCY_OFF = Pattern("1391859323067.png").similar(0.95)
    TRANSPARENCY_ON = Pattern("1391859300044.png").similar(0.95)
    OK_LIGHTBOX_BORDER_H = Pattern("1391941926753.png").similar(0.78)
    OK_LIGHTBOX_BORDER_W = Pattern("1391942228532.png").similar(0.78)

    FOREST_ERROR = Pattern("1390654120149.png").similar(0.91)


"""
    Exceptions
"""


class CraftException(Exception):
    pass


class UnknownDirectionException(CraftException):
    pass


class ImageNotFound(CraftException):
    pass


class Point(object):
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y

    def __str__(self):
        return "Point(%d, %d)" % (self.x, self.y)


class SearchStatus(object):
    PINE_IN_5_STEPS = "Tree is in 5 steps"
    PINE_IN_FRONT = "Tree is in front"
    PINE_ON_THE_RIGHT = "Tree is on the right"
    PINE_ON_THE_LEFT = "Tree is on the left"

    OAK_IN_5_STEPS = "Oak is in 5 steps"
    OAK_IN_FRONT = "Oak is in front"
    OAK_ON_THE_RIGHT = "Oak is on the right"
    OAK_ON_THE_LEFT = "Oak is on the left"


class Constants(object):
    MAIN_WINDOW_WIDTH = 480
    MAIN_WINDOW_HEIGHT = 310

    ARROW_TRUE_HEIGHT = 17
    HEIGHT_BETWEEN_ARROW_AND_PLAYER = 7
    PLAYER_TRUE_HEIGHT = 62
    PLAYER_TRUE_WIDTH = 19

    PLAYER_HEIGHT = 72
    PLAYER_WIDTH = 35
    Y_OFFSET = 40

    LEFT = "Left"
    RIGHT = "Right"


class Resources(object):
    PINES = [Images.PINE_TREE, Images.PINE_TREE2, Images.PINE_TREE3]
    OAKS = [Images.OAK_TREE, Images.OAK_TREE2, Images.OAK_TREE3]
    ALL_TREES = PINES + OAKS


class Direction(object):
    N = 'North'
    S = 'South'
    W = 'West'
    E = 'East'
    NW = 'North-West'
    SW = 'South-West'
    NE = 'North-East'
    SE = 'South-East'

    @classmethod
    def get_all_players_directions(cls):
        return [cls.N, cls.NE, cls.SE, cls.S, cls.SW, cls.NW]

    @classmethod
    def get_all_directions(cls):
        return [cls.N, cls.NE, cls.E, cls.SE, cls.S, cls.SW, cls.W, cls.NW]

    @classmethod
    def get_opposite_direction(cls, direction):
        opposite = None
        if cls.N == direction:
            opposite = cls.S
        elif cls.S == direction:
            opposite = cls.N
        elif cls.NW == direction:
            opposite = cls.SE
        elif cls.NE == direction:
            opposite = cls.SW
        elif cls.SE == direction:
            opposite = cls.NW
        elif cls.SW == direction:
            opposite = cls.NE

        if opposite:
            return opposite
        else:
            raise UnknownDirectionException

    @classmethod
    def get_random_direction(cls, directions=None, skip=None):
        if not directions:
            directions = cls.get_all_directions()
        if skip:
            directions = [d for d in directions if d not in skip]
        return random.choice(directions)


DIRECTION_2_POINT = {
    Direction.NW: Images.NW_POINT,
    Direction.SW: Images.SW_POINT,
    Direction.NE: Images.NE_POINT,
    Direction.SE: Images.SE_POINT,
    Direction.N: Images.NW_POINT,
    Direction.S: Images.SW_POINT,
    Direction.W: Images.NW_POINT,
    Direction.E: Images.NE_POINT,
}

PLAYER_DIRECTIONS = {
    Images.N: Direction.N,
    Images.NE: Direction.NE,
    Images.SE: Direction.SE,
    Images.S: Direction.S,
    Images.SW: Direction.SW,
    Images.NW: Direction.NW
}

DEBUG = True
# DEBUG = False


"""
    Logger
"""


class Logger(object):
    def log(self, *msgs):
        if DEBUG:
            msg = "%s: %s" % (strftime("%Y%m%d%H%M%S"),
                              " ".join([str(msg) for msg in msgs]))
            print msg


"""
    Wrappers
"""


def expection_wrapper(func):
    def wrapper(*args, **kwargs):
        def check_if_flash_error(e):
            def is_flash_error():
                return exists(Images.FOREST_ERROR, 1)

            def is_window_exists():
                return exists(Images.MAIN_WINDOW, 1)

            if is_flash_error() and not is_window_exists():
                while (is_flash_error() and not is_window_exists()):
                    sleep(1)

                try:
                    return func(*args, **kwargs)
                except FindFailed, e:
                    raise ImageNotFound("Image not found" + str(e))
            else:
                raise ImageNotFound("Image not found" + str(e))

        try:
            return func(*args, **kwargs)
        except FindFailed, e:
            check_if_flash_error(e)
        except ImageNotFound, e:
            check_if_flash_error(e)

    return wrapper


def logging_wrapper(func):
    def wrapper(*args, **kwargs):
        value = None
        if DEBUG:
            logger = Logger()
            s_args = ", ".join([str(arg) for arg in args])
            s_kwargs = ", ".join([str(arg) for arg in kwargs])
            logger.log("* EXECUTE: %s(%s, %s)" % (func.func_name,
                                                  s_args,
                                                  s_kwargs))
            before = time()
            value = func(*args, **kwargs)
            after = time()
            exec_time = after - before
            logger.log("* RETURN:  %s -> %s exec_time: %s" % (func.func_name,
                                                              value,
                                                              exec_time))
        else:
            value = func(*args, **kwargs)
        return value

    return wrapper


class Timeout(object):
    EXISTS = 1


"""
    Sikuli actions
"""


class Sikuli(object):
    KEY_UP = Key.UP
    KEY_DOWN = Key.DOWN
    KEY_LEFT = Key.LEFT
    KEY_RIGHT = Key.RIGHT
    KEY_END = Key.END
    KEY_PAGE_DOWN = Key.PAGE_DOWN
    KEY_CTRL = Key.CTRL
    KEY_F5 = Key.F5

    def capture(self, x, y, w, h):
        return Pattern(Screen().capture(x, y, w, h)).similar(0.99)

    def type(self, text):
        type(text)

    @expection_wrapper
    def type_to_image(self, image, text):
        type(image, text)

    @expection_wrapper
    def find(self, image):
        return find(image)

    @expection_wrapper
    def get_pattern(self, image):
        return Pattern(image)

    @expection_wrapper
    def find_all(self, image):
        finder = findAll(image)
        images = []
        while (finder.hasNext()):
            images.append(finder.next())
        return images

    @expection_wrapper
    def click(self, image):
        click(image)

    def wait_for_not_visible(self, image):
        waitVanish(image)

    @expection_wrapper
    def double_click(self, image):
        doubleClick(image)

    @expection_wrapper
    def hover(self, image):
        hover(image)

    @expection_wrapper
    def _set_target_offset(self, image, point):
        try:
            print "-" * 50
            print image
            if isinstance(image, Match):
                target = image.getTarget()
            elif isinstance(image, Pattern):
                image = self.get_pattern(image)
                target = self.find(image).getTarget()
            else:
                raise Exception('Passed argument is not supported - %s' % image)

            print target.x, target.y
            print Location(target.x + point.x, target.y + point.y)
            print "*" * 50
            return Location(target.x + point.x, target.y + point.y)
        except Exception, e:
            self.log(e)
            print "+" * 50
            raise ImageNotFound

    @expection_wrapper
    def _hover_by_offset(self, image, point):
        image = self._set_target_offset(image, point)
        hover(image)

    def refresh(self):
        if self.exists(Images.AXE):
            self.click(Images.AXE)
        type(self.KEY_F5)

    def _click_by_offset(self, image, point):
        image = self._set_target_offset(image, point)
        self.click(image)

    def _double_click_by_offset(self, image, point):
        image = self._set_target_offset(image, point)
        self.double_click(image)

    def exists(self, image):
        return exists(image, Timeout.EXISTS) is not None

    def _click_and_not_visible(self, image):
        for _ in range(5):
            try:
                if self.exists(image):
                    self.click(image)

                if not self.exists(image):
                    return True
            except ImageNotFound, e:
                self.log("Exception", e)
            finally:
                sleep(0.1)

        return False

    @expection_wrapper
    def _click(self, image_before, image_after):
        for _ in range(5):
            try:
                if self.exists(image_before):
                    self.click(image_before)
                if not self.exists(image_before) and self.exists(image_after):
                    return True
            except ImageNotFound:
                pass
            finally:
                sleep(0.1)
        return False

    def _mouse_wheel_up(self, image, times):
        region = self.find(image)
        region.wheel(WHEEL_UP, times)

    def _mouse_wheel_down(self, image, times):
        region = self.find(image)
        region.wheel(WHEEL_DOWN, times)

    @expection_wrapper
    def wait(self, image, timeout=None):
        if timeout:
            wait(image, timeout)
        else:
            wait(image)


"""
    ApehaFlash
"""


class ApehaFlash(Sikuli, Logger):
    @logging_wrapper
    def capture_player(self):
        center_point = self.get_screen_center_point()
        width = Constants.PLAYER_WIDTH * 6
        height = Constants.PLAYER_TRUE_HEIGHT
        start_x = center_point.x - width / 2
        start_y = center_point.y - Constants.PLAYER_TRUE_HEIGHT - \
                  Constants.HEIGHT_BETWEEN_ARROW_AND_PLAYER - \
                  Constants.HEIGHT_BETWEEN_ARROW_AND_PLAYER
        return self.capture(start_x, start_y, width, height)

    @logging_wrapper
    def _shake_screen(self):
        offset = 5
        self.click(Images.MAIN_WINDOW)
        self._mouse_wheel_down(Images.MAIN_WINDOW, offset)
        self._mouse_wheel_up(Images.MAIN_WINDOW, offset)
        self._mouse_wheel_down(Images.MAIN_WINDOW, offset)

    @logging_wrapper
    def get_target(self, sth):
        if 'getTarget' not in dir(sth):
            sth = self.find(sth)
        return sth.getTarget()

    @logging_wrapper
    def get_point(self, image):
        try:
            target = self.get_target(image)
        except ImageNotFound:
            self._shake_screen()
            target = self.get_target(image)
        return Point(target.getX(), target.getY())

    @logging_wrapper
    def get_screen_center_point(self):
        p1 = self.get_point(Images.NW_POINT)
        p2 = self.get_point(Images.SE_POINT)
        x = (p2.x - p1.x) / 2 + p1.x
        y = (p2.y - p1.y) / 2 + p1.y
        return Point(x, y)

    @logging_wrapper
    def get_distance(self, p1, p2):
        a = p1.x - p2.x
        b = p1.y - p2.y
        return math.sqrt(float(a * a + b * b))

    @logging_wrapper
    def get_difference_between(self, p1, p2):
        return Point(p2.x - p1.x, p2.y - p1.y)


class FlashMovement(ApehaFlash):
    @logging_wrapper
    def is_another_group_around(self):
        self.click(Images.MAIN_WINDOW)

        for _ in range(3):
            self.type("i")
            if not self.exists(Images.MY_GROUP):
                return True
            sleep(0.3)

        self.type("i")
        return not self.exists(Images.MY_GROUP)

    @logging_wrapper
    def search_for_groups(self):
        found = False
        while (self.exists(Images.MAIN_WINDOW)):
            sleep(1.0)
            found = self.is_another_group_around()
            if found:
                if self.exists(Images.WALK):
                    self.click(Images.WALK)
                break

        if found:
            self.log("Found another group")
        else:
            self.log("Closed unexpectedly")

    @logging_wrapper
    def is_moving_after_func(self, func, *args):
        tmp_image = self.capture_player()
        func(*args)
        return self.is_moving(tmp_image)

    @logging_wrapper
    def is_moving(self, tmp_image=None):
        if not tmp_image:
            tmp_image = self.capture_player()
        for _ in range(5):
            sleep(0.01)
            if not self.exists(tmp_image):
                return True
        return False

    @logging_wrapper
    def get_direction_with_offset(self, direction):
        is_nw = direction == Direction.NW
        is_ne = direction == Direction.NE
        is_sw = direction == Direction.SW
        is_se = direction == Direction.SE
        is_s = direction == Direction.S
        is_n = direction == Direction.N
        is_w = direction == Direction.W
        is_e = direction == Direction.E

        min_x = 30
        max_x = 120
        min_y = 20
        max_y = 90

        if is_n or is_s:
            min_x = int(Constants.MAIN_WINDOW_WIDTH / 3)
            max_x = int(Constants.MAIN_WINDOW_WIDTH / 3 * 2)
            min_y = min_y / 2
            if is_n:
                max_y = 90 / 2
            else:
                max_y = 90 - min_y
        elif is_e or is_w:
            min_x = min_x / 2
            max_x = max_x / 3
            min_y = int(Constants.MAIN_WINDOW_HEIGHT / 3)
            max_y = int(Constants.MAIN_WINDOW_HEIGHT / 3 * 2)

        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)
        if is_n:
            return Point(x, y)
        elif is_s:
            return Point(x, -y)
        elif is_w:
            return Point(x, y)
        elif is_e:
            return Point(-x, y)
        elif is_nw:
            return Point(x, y)
        elif is_ne:
            return Point(-x, y)
        elif is_sw:
            return Point(x, -y)
        elif is_se:
            return Point(-x, -y)

    @logging_wrapper
    def get_player_direction(self):
        images_list = [Images.S, Images.SW, Images.NW,
                       Images.NE, Images.SE, Images.N]

        for image in images_list:
            if self.exists(image):
                return PLAYER_DIRECTIONS[image]

        raise UnknownDirectionException("Could determine player's direction")

    @logging_wrapper
    def move(self, directions=None):
        self.click_ok()

        if not directions:
            dir1 = Direction.get_random_direction()
            dir2 = Direction.get_random_direction(skip=[dir1])
            dir3 = Direction.get_random_direction(skip=[dir1, dir2])
            dir4 = Direction.get_random_direction(skip=[dir1, dir2, dir3])
            directions = [dir1, dir2, dir3, dir4]

        def double_click_offset(image, direction):
            point = self.get_direction_with_offset(direction)
            self._double_click_by_offset(image, point)

        img_before_movement = self.capture_player()
        for direction in directions:
            image = self.get_pattern(DIRECTION_2_POINT[direction])
            print image

            tmp_image = self.capture_player()
            for _ in range(5):
                print image
                double_click_offset(image, direction)
                sleep(0.1)
                if not self.exists(tmp_image):
                    self.wait_for_stop()
                    break

        return not self.exists(img_before_movement)

    @logging_wrapper
    def wait_for_stop(self):
        before = time()
        after = time()

        while (self.is_moving()):
            if after - before > 5 * 60:
                break
            sleep(0.5)
            after = time()

    @logging_wrapper
    def get_turning_direction(self, turn):
        """ Returns Direction where turn to
        Parameter 'turn' should be Constants.LEFT or Constants.RIGHT
        """
        cur_direction = self.get_player_direction()
        directions = Direction.get_all_players_directions()
        index = directions.index(cur_direction)
        offset = 1 if turn == Constants.RIGHT else -1
        index += offset
        if index >= len(directions):
            index = 0
        elif index < 0:
            index = len(directions) - 1

        return directions[index]


class CraftSearch(FlashMovement):
    default_trees = Resources.OAKS

    #     default_trees = Resources.PINES

    @logging_wrapper
    def _click_transparency_if_needed(self):
        if not self.exists(Images.TRANSPARENCY_ON):
            self._click(Images.TRANSPARENCY_OFF, Images.TRANSPARENCY_ON)

    @logging_wrapper
    def click_search(self):
        self._click(Images.SEARCH, Images.SEARCH_TIMER)

    @logging_wrapper
    def found_nothing(self):
        return self.exists(Images.NOTHING_WAS_FOUND)

    @logging_wrapper
    def is_ok_lightbox_visible(self):
        return self.exists(Images.OK_LIGHTBOX_BORDER_H) or \
               self.exists(Images.OK_LIGHTBOX_BORDER_W)

    @logging_wrapper
    def wait_for_ok(self):
        for _ in range(5):
            try:
                self.log("Waiting for ok")
                self.wait(Images.OK, 35)
                break
            except ImageNotFound, e:
                self.log(e)
                if self.is_ok_lightbox_visible():
                    self.log("Shaking")
                    self._shake_screen()

    @logging_wrapper
    def click_ok(self):
        exists = self.exists(Images.OK)
        while (exists):
            try:
                if self.is_ok_lightbox_visible():
                    self.log("Clicking...OK")
                    self.click(Images.OK)
            except Exception, e:
                self.log("Exception", e)
            finally:
                sleep(0.1)
                exists = self.exists(Images.OK)

    @logging_wrapper
    def get_found_status(self):
        if self.exists(Images.PINE_IN_5_STEPS):
            return SearchStatus.PINE_IN_5_STEPS
        elif self.exists(Images.PINE_IN_FRONT):
            return SearchStatus.PINE_IN_FRONT
        elif self.exists(Images.PINE_ON_LEFT):
            return SearchStatus.PINE_ON_THE_LEFT
        elif self.exists(Images.PINE_ON_RIGHT):
            return SearchStatus.PINE_ON_THE_RIGHT
        elif self.exists(Images.OAK_IN_5_STEPS):
            return SearchStatus.OAK_IN_5_STEPS
        elif self.exists(Images.OAK_IN_FRONT):
            return SearchStatus.OAK_IN_FRONT
        elif self.exists(Images.OAK_ON_LEFT):
            return SearchStatus.OAK_ON_THE_LEFT
        elif self.exists(Images.OAK_ON_RIGHT):
            return SearchStatus.OAK_ON_THE_RIGHT
        else:
            p = self.get_point(self.find(Images.NW_POINT))
            f = self.capture(p.x, p.y, 480, 310)
            self.log("UNKOWN STATUS:", f)

            return None

    @logging_wrapper
    def search_for_res(self, times=1):
        def wait_for_search_btn_is_visible():
            max_seconds = 60
            before = time()
            after = time()

            while (not self.exists(Images.SEARCH) and not self.exists(Images.OK)):
                if after - before > max_seconds:
                    raise ImageNotFound
                sleep(1)
                after = time()

        found_tree = False

        status = None
        self.log("Searching")
        i = 0

        self.click_ok()

        while (not found_tree):
            try:
                if i >= times:
                    found_tree = True

                self._click(Images.SEARCH, Images.SEARCH_TIMER)

                wait_for_search_btn_is_visible()

                if not self.exists(Images.OK) and self.is_ok_lightbox_visible():
                    self._shake_screen()

                found_tree = not self.found_nothing()

                self.log(found_tree)
                if found_tree:
                    status = self.get_found_status()

                self.click_ok()

                i += 1

                if i >= times:
                    found_tree = True
            except ImageNotFound:
                sleep(3)
            #                 self.refresh()
            #                 sleep(15)
            #                 if self.exists(Images.AXE):
            #                     self.click(Images.AXE)

        self.log("DONE: searching")
        return status

    @logging_wrapper
    def find_tree_by_point(self, point, trees_images=None):
        trees = self.find_trees(trees_images=trees_images)
        closest_tree = None
        closest_dist = None

        for tree in trees:
            #             self.log("hover", tree)
            #             self.hover(tree)
            tree_point = self.get_point(tree)
            #             self.log(11)
            cur_dist = self.get_distance(tree_point, point)
            #             self.log(22)
            #             closest_dist = self.get_distance(self.get_point(trees[0]), point)
            #             self.log(33)
            #             self.log("find_tree_by_point", cur_dist, closest_dist)
            if not closest_dist:
                closest_dist = cur_dist

            if cur_dist <= closest_dist and cur_dist < 100:
                closest_tree = tree
                closest_dist = cur_dist

        return closest_tree

    @logging_wrapper
    def is_point_inside_5_step_area(self, point):
        # SE quadrant of hexogen
        point_center = Point(0, 0)
        point_south = Point(0, 145)
        point_east = Point(200, 0)
        point_south_east = Point(207, 73)

        cp = self.get_screen_center_point()
        p = self.get_difference_between(cp, point)
        x, y = abs(p.x), abs(p.y)

        # 2 triangles inside quadrant, looping over them
        for p1, p2, p3 in [(point_center, point_south_east, point_south),
                           (point_center, point_south_east, point_east)]:
            x1, y1 = p1.x, p1.y
            x2, y2 = p2.x, p2.y
            x3, y3 = p3.x, p3.y
            #             self.log("x1=%d, y1=%d" % (x1,y1))
            #             self.log("x2=%d, y2=%d" % (x2,y2))
            #             self.log("x3=%d, y3=%d" % (x3,y3))
            det = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)

            alpha = float((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / det
            beta = float((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / det
            gamma = 1.0 - alpha - beta

            self.log("is_point_inside", p, alpha, beta, gamma)
            if 0.0 <= alpha <= 1.0 and \
                                    0.0 <= beta <= 1.0 and \
                                    0.0 <= gamma <= 1.0:
                return True

        return False

    @logging_wrapper
    def find_trees(self, trees_images=None, only_trees_in_5_steps=True):
        if not trees_images:
            trees_images = self.default_trees

        self._click_transparency_if_needed()
        trees = []
        for tree in trees_images:
            try:
                found_trees = self.find_all(tree)
                if only_trees_in_5_steps:
                    found_trees = [t for t in found_trees \
                                   if self.is_point_inside_5_step_area(
                            self.get_point(t)
                        )
                                   ]
                if len(found_trees) > 0:
                    trees += found_trees
            except ImageNotFound:
                pass
        return trees

    @logging_wrapper
    def get_sorted_trees(self, trees):
        cp = self.get_screen_center_point()

        def get_distance(t):
            tp = self.get_point(t)
            return self.get_distance(cp, tp)

        trees = sorted(trees, key=get_distance)
        return trees

    @logging_wrapper
    def get_closest_tree(self, trees_images=None):
        if not trees_images:
            trees_images = Resources.ALL_TREES
        trees = self.find_trees(trees_images=trees_images)
        trees = self.get_sorted_trees(trees)
        return trees[0] if len(trees) > 0 else None

    @logging_wrapper
    def _pivot_to(self, direction):
        dirs = Direction.get_all_players_directions()
        cur_dir = self.get_player_direction()

        while (cur_dir != direction):
            cdi = dirs.index(cur_dir)
            tdi = dirs.index(direction)
            times = tdi - cdi
            self.log("Times to pivot:", times)
            if times != 0:
                self.click(Images.MAIN_WINDOW)
                key = self.KEY_RIGHT if times > 0 else self.KEY_LEFT
                self.type(key * abs(times))
                sleep(0.2)

            cur_dir = self.get_player_direction()

    @logging_wrapper
    def go_to_tree_upfront(self, tree, diff_point=None):
        directions = []
        self.log("go_to_tree_upfront", diff_point)
        if diff_point and diff_point.x < 0:
            directions = [Direction.N, Direction.NW, Direction.SW]
        elif diff_point and diff_point.x > 0:
            directions = [Direction.N, Direction.NE, Direction.SE]
        else:
            directions = [Direction.N, Direction.NE, Direction.SE, Direction.SW, Direction.NW]

        for direction in directions:
            self.log("go_to_tree_upfront", direction)
            tmp_img = self.capture_player()
            is_moving = self.is_moving_after_func(self.double_click_near_tree,
                                                  tree,
                                                  direction)
            if is_moving:
                self.wait_for_stop()

            if not self.exists(tmp_img) and self.is_near():
                try:
                    self.get_player_direction()
                    return True
                except UnknownDirectionException:
                    pass

            if is_moving:
                tree = self.get_closest_tree()

        return False

    @logging_wrapper
    def is_near(self, tree=None):
        minimal_distance = 60

        if not tree:
            tree = self.get_closest_tree()

        tp = self.get_point(tree)
        cp = self.get_screen_center_point()

        distance = self.get_distance(cp, tp)
        return distance < minimal_distance

    @logging_wrapper
    def _get_direction_to_pivot(self):
        tree = self.get_closest_tree()
        self.hover(tree)
        assert self.is_near(tree)
        tp = self.get_point(tree)  # center point of tree
        cp = self.get_screen_center_point()
        tp.y = tp.y + 13  # fixing y, point root of tree
        tx, ty = tp.x, tp.y
        cx, cy = cp.x, cp.y
        dx = tx - cx
        dy = ty - cy

        self.log(cp, tp)
        self.log(dx, dy)
        if abs(dx) <= Constants.PLAYER_TRUE_WIDTH / 2:
            if dy > 0:
                degrees = 90
            else:
                degrees = 180
        else:
            degrees = abs(math.degrees(math.atan(float(dy) / dx)))
            if tx > cx and ty > cy:
                degrees += 90
            elif tx > cx and ty < cy:
                degrees += 180
            elif tx < cx and ty < cy:
                degrees = 270 + 90 - degrees

        self.log("Degrees", degrees)

        if 0 < degrees < 90:
            return Direction.SW
        elif 90 < degrees < 180:
            return Direction.SE
        elif 180 < degrees < 270:
            return Direction.NE
        elif 270 < degrees < 360:
            return Direction.NW
        elif degrees == 90:
            return Direction.S
        else:
            return Direction.N

    @logging_wrapper
    def __get_tree_offset_point_by(self, direction):
        x = 38
        pn = Point(x, 4)  # point in I and II quadrant(north)
        ps = Point(x, 24)  # point in III and IV quadrant(south)
        point = None
        if direction == Direction.NE:
            point = Point(pn.x, -pn.y)
        elif direction == Direction.SE:
            point = Point(ps.x, ps.y)
        elif direction == Direction.SW:
            point = Point(-ps.x, ps.y)
        elif direction == Direction.NW:
            point = Point(-pn.x, -pn.y)
        elif direction == Direction.N:
            point = Point(0, -30)
        elif direction == Direction.S:
            point = Point(0, 30)
        else:
            msg = "Action for chosen direction{%s} is not supported" % direction
            raise NotImplementedError(msg)
        return point

    @logging_wrapper
    def double_click_near_tree(self, tree, direction):
        point = self.__get_tree_offset_point_by(direction)
        self._double_click_by_offset(tree, point)

    @logging_wrapper
    def click_near_tree(self, tree, direction):
        point = self.__get_tree_offset_point_by(direction)
        self._click_by_offset(tree, point)

    @logging_wrapper
    def come_to_tree(self, tree=None):
        if not tree:
            tree = self.get_closest_tree()


class CraftMine(CraftSearch):
    TIME_TO_MINE = 5.2 * 60

    @logging_wrapper
    def put_tool_if_necessary(self):
        has_tool = self.exists(Images.AXE)
        if has_tool:
            return
        else:
            while (not has_tool):
                new_window = False
                try:
                    self._click(Images.BACKPACK, Images.BP_TOOLS)
                    new_window = True
                    has_tool = self.exists(Images.AXE)
                    if not has_tool:
                        self.wait(Images.BP_TOOLS, 20)
                        self.click(Images.BP_TOOLS)
                        self.wait(Images.BP_PUT, 20)
                        self._mouse_wheel_down(Images.BP_PUT, 50)
                        for _ in range(10):
                            sleep(1)
                            puts = self.find_all(Images.BP_PUT)
                            puts = sorted(puts, key=lambda x: self.get_point(x).y)
                            if len(puts) > 0:
                                self.click(puts[-1])
                                break
                except:
                    pass
                finally:
                    if new_window:
                        type("w", self.KEY_CTRL)
                        self.wait(Images.MAIN_WINDOW, 20)
                    has_tool = self.exists(Images.AXE)

    @logging_wrapper
    def craft(self):
        def wait_for_craft_btn_is_visible():
            max_seconds = 60 * 10
            before = time()
            after = time()
            while (not self.exists(Images.CRAFT) or self.exists(Images.CRAFT_TIMER)):
                self.log("Waiting for Craft is ended")
                sleep(1)
                after = time()
                if after - before > max_seconds:
                    raise ImageNotFound

        tree_is_standing = True

        self.log("Crafting")
        self.click_ok()

        while (tree_is_standing):
            try:
                was_clicked = self._click(Images.CRAFT, Images.CRAFT_TIMER)

                if self.exists(Images.NEED_AN_AXE):
                    self.click_ok()
                    self.put_tool_if_necessary()
                    was_clicked = self._click(Images.CRAFT, Images.CRAFT_TIMER)

                self.log("Clicked", was_clicked)
                self.log(tree_is_standing)

                if was_clicked:
                    wait_for_craft_btn_is_visible()
                    self.log(tree_is_standing)

                    if self.exists(Images.CRAFT):
                        if not self.exists(Images.OK) and \
                                self.is_ok_lightbox_visible():
                            self._shake_screen()
                        self.click_ok()

                else:
                    tree_is_standing = False
            except ImageNotFound:
                sleep(3)
            #                 self.refresh()
            #                 sleep(15)
            #                 if self.exists(Images.AXE):
            #                     self.click(Images.AXE)

        self.log("DONE: crafting")


class Movement(object):
    def next_direction(self):
        raise NotImplementedError


class LinearMovement(object):
    def __init__(self):
        self.index = 0
        self.times_per_direction = 20

        # map: Polesje
        self.directions = [
            [Direction.NW],
            [Direction.SW],
            [Direction.SE],
            [Direction.NE]
        ]
        # backwards

    #        self.directions = [
    #                            [Direction.SE],
    #                            [Direction.SW],
    #                            [Direction.NW],
    #                            [Direction.NE],
    #                           ]

    # temnqe 4ashjobq
    #         self.directions = [
    #                            [Direction.SE, Direction.SE, Direction.E],
    #                            [Direction.S, Direction.SW],
    #                            [Direction.NW, Direction.NW, Direction.NW],
    #                            [Direction.NE]
    #                           ]

    # zigzag
    #        self.directions = [
    #                           [Direction.NW],
    #                           [Direction.SW],
    #                           [Direction.N],
    #                           [Direction.SE],
    #                           [Direction.NE],
    #                           [Direction.S],
    #                           ]
    # Direction: narrow romb
    #         self.directions = [
    #                            [Direction.N, Direction.NW],
    #                            [Direction.S, Direction.SW],
    #                            [Direction.S, Direction.SE],
    #                            [Direction.N, Direction.NE]
    #                            ]

    #         self.directions = [
    #                            [Direction.NE, Direction.N],
    #                            ]

    def next_direction(self):
        dir_count = len(self.directions)

        if self.index >= self.times_per_direction * dir_count:
            self.index = 0

        direction = None
        directions = None
        for i in range(dir_count):
            if i * self.times_per_direction <= self.index and \
                            self.index < (i + 1) * self.times_per_direction:
                directions = self.directions[i]
                break

        if not directions:
            directions = self.directions[0]

        inner_dir_count = len(directions)
        if inner_dir_count == 1:
            direction = directions[0]
        else:
            direction = directions[self.index % inner_dir_count]

        self.index += 1

        return direction


class RandomMovement(object):
    def next_direction(self):
        return Direction.get_random_direction()


class CraftMain(CraftMine, FlashMovement):
    TIMES = 10
    AREA_MOVEMENT = 1
    MOVEMENT = LinearMovement()

    @logging_wrapper
    def go_to_place_in_forest(self, directions):
        self.move(directions)
        self.wait_for_stop()

    @logging_wrapper
    def find_tree_and_craft_in_5_steps(self, trees_images=None):
        count = len(self.find_trees(trees_images=trees_images))
        self.log(count)
        for i in range(1, count):
            trees = self.get_sorted_trees(self.find_trees(trees_images=trees_images))
            if i >= len(trees):
                return False
            tree = trees[i]

            point_tree = self.get_point(tree)
            point_closest_tree = self.get_point(trees[0])
            diftree = self.get_difference_between(point_tree,
                                                  point_closest_tree)
            status = self.go_to_tree_and_search(tree, trees_images)
            if status:
                self.click_ok()
                if status in [SearchStatus.PINE_IN_FRONT,
                              SearchStatus.OAK_IN_FRONT]:
                    self.craft()
                    return True
                elif status in [SearchStatus.PINE_ON_THE_LEFT,
                                SearchStatus.OAK_ON_THE_LEFT]:
                    direction = self.get_turning_direction(Constants.LEFT)
                    self._pivot_to(direction)
                    self.craft()
                    return True
                elif status in [SearchStatus.PINE_ON_THE_RIGHT,
                                SearchStatus.OAK_ON_THE_RIGHT]:
                    direction = self.get_turning_direction(Constants.RIGHT)
                    self._pivot_to(direction)
                    self.craft()
                    return True
            else:
                self.click_ok()
            self.log("=" * 50)
            new_closest = self.get_point(self.get_closest_tree(trees_images))
            self.log(1)
            diff_point = Point(
                new_closest.x + diftree.x,
                new_closest.y + diftree.y)
            prev_tree = self.find_tree_by_point(diff_point, trees_images)

            self.log("Prev tree:", prev_tree)
            self.go_to_tree_upfront(prev_tree)
            self.log("=" * 50, "END")

        return False

    @logging_wrapper
    def go_to_tree_and_search(self, tree=None, trees_images=None):
        if not tree:
            tree = self.get_closest_tree(trees_images)
        if self.go_to_tree_upfront(tree):
            direction = self._get_direction_to_pivot()
            self._pivot_to(direction)
            return self.search_for_res(self.TIMES)
        else:
            return None

    @logging_wrapper
    def search_in_current_area(self):
        self.click_ok()
        status = self.go_to_tree_and_search()

        if status and DEBUG:
            p = self.get_point(self.find(Images.NW_POINT))
            f = self.capture(p.x, p.y, 480, 310)
            self.log("SCREEN:", f)

        if status:
            self.log(status)
            self.click_ok()

        if status in [SearchStatus.PINE_IN_FRONT,
                      SearchStatus.OAK_IN_FRONT]:
            self.craft()
            return True
        elif status in (SearchStatus.PINE_ON_THE_LEFT,
                        SearchStatus.OAK_ON_THE_LEFT):
            direction = self.get_turning_direction(Constants.LEFT)
            self._pivot_to(direction)
            self.craft()
            return True
        elif status in (SearchStatus.PINE_ON_THE_RIGHT,
                        SearchStatus.OAK_ON_THE_RIGHT):
            direction = self.get_turning_direction(Constants.RIGHT)
            self._pivot_to(direction)
            self.craft()
            return True
        elif status == SearchStatus.PINE_IN_5_STEPS:
            return self.find_tree_and_craft_in_5_steps(Resources.PINES)
        else:
            return False

    @logging_wrapper
    def move_to_other_location(self, is_good_direction=True):
        back_times = 10
        times_per_dir = 0
        moved = False

        prev_directions = []
        while (not moved):
            direction = self.MOVEMENT.next_direction()

            if is_good_direction:
                if times_per_dir <= self.AREA_MOVEMENT:
                    directions = [direction] * self.AREA_MOVEMENT
                else:
                    directions = [Direction.get_random_direction(
                        skip=prev_directions)] * times_per_dir
            else:
                directions = [Direction.get_opposite_direction(direction)]

            moved = self.move(directions)

            if moved and not is_good_direction:
                for _ in range(1, back_times):
                    if not self.move(directions):
                        break

            prev_directions += directions
            times_per_dir += 1
            self.log("move_to_other_location TIMES", times_per_dir)

        self.wait_for_stop()

    @logging_wrapper
    def try_to_craft(self):
        while (True):
            try:
                val = self.search_in_current_area()
                if val:
                    self.search_in_current_area()
            except Exception, e:
                self.log(e)
                traceback.print_exc()
            finally:
                try:
                    self.move_to_other_location()
                    while (True):
                        trees = len(self.find_trees())

                        good_number_of_trees = 8
                        is_good_area = trees > 2 and \
                                       trees <= good_number_of_trees
                        #                             and \
                        #                             not self.exists(Images.ROAD_PAVEMENT)
                        is_good_direction = trees < good_number_of_trees * 2

                        self.log("is_good_area", is_good_area)
                        self.log("is_good_direction", is_good_direction)
                        if is_good_area:
                            break
                        else:
                            self.move_to_other_location(is_good_direction)
                except Exception, e:
                    self.log(e)
                    traceback.print_exc()
                    sleep(3)


if __name__ == "__main__":
    # Main crafting logic
    main = CraftMain()
    # main.login()
    # main.check_my_set()
    # main.leave_city()
    dirs = [Direction.SW, Direction.NW] * 500
    dirs = [Direction.NW] * 200
    dirs = [Direction.NW] * 100
    dirs = [Direction.NW] * 100
    dirs = [Direction.NE] * 50
    # back to city
    dirs = [Direction.W] * 100 + [Direction.NW] * 150
    # dirs = [Direction.NE]*20 + [Direction.SE]*200
    dirs = [Direction.NE, ]

    #     main._click_and_not_visible(Pattern("1401007414273.png").similar(0.87))
    #     main._click_and_not_visible(Pattern("1401007572182.png").similar(0.87))
    #     main._click_and_not_visible(Pattern("1401007851994.png").similar(0.87))
    #     main._click_and_not_visible(Pattern("1401008117882.png").similar(0.88))

    # print dirs
    # main.go_to_place_in_forest(dirs)
    # main.MOVEMENT.times_per_direction = 2
    #     main.move_to_other_location()
    # main.move(dirs[:1])
    main.try_to_craft()
    # main.click_ok()
    # main.craft()
    # print main.get_closest_tree()
    # print [main.get_distance(main.get_screen_center_point(), main.get_point(t)) for t in main.get_sorted_trees(main.find_trees())]
    # for t in main.get_sorted_trees(main.find_trees()):
    #     main.hover(t)
    # print len(main.find_trees())
    # main.move([Direction.N]*3)
    # main.search_for_res(5)
    # main.craft()
    # main.go_to_tree_and_search()
    # tree = main.get_closest_tree()
    # direction = main.go_to_tree_upfront(tree)
    # direction = main._get_direction_to_pivot()
    # main.get_player_direction()
    # main._pivot_to(direction)
    #     main.find_tree_and_craft_in_5_steps()
    # main.search_in_current_area()
    # main.hover(main.get_closest_tree())
    # main.get_distance(main.get_point(main.get_closest_tree()), main.get_screen_center_point())
    # main.move([Direction.NW]*20)# to random direction

    # search_for_res(10)
    # _craft()
    # search_for_groups()

    # direction = random.choice([Direction.NW,Direction.EW,Direction.NE,Direction.SE])
    # for _ in range(30):
    #    move(Direction.NW)
    # move(Direction.SE)
    # self.log(hover(__get_closest_tree())
    # get_to_tree_upfront()
    # [hover(tree) for tree in find_trees()]
    # search_for_tree()
    # __get_closest_tree()
    # __get_center_point()
    # get_to_tree_upfront()
    # print exists()
    # kraft()

    # direction =  _get_direction_to_pivot()
    # print direction
    # __pivot_to(direction)

    # TEST: find tree closest to coordinates
    # click_search = CraftSearch()
    # center = click_search.get_screen_center_point()
    # ftree = click_search.find_tree_by_point(center)
    # click_search.hover(ftree)
    # # print "1:", ftree
    # # print "2:", click_search.get_closest_tree()
    # assert str(ftree) == str(click_search.get_closest_tree())
    # END

    # TEST: go to tree and click_search
    # main = CraftMain()
    # tree = main.get_closest_tree()
    # if main.go_to_tree_upfront(tree):
    #     direction = main._get_direction_to_pivot()
    #     main._pivot_to(direction)
    # else:
    #     assert False
    # END

    # TEST: find center 10 times
    '''
    for i in range(100):
        print i
        print main.get_screen_center_point()
    '''
    # END

    # TEST: get direction to pivot
    #     print main._get_direction_to_pivot()
    # END

    # TEST: basic images are visible
    '''
    for i in [Images.NW_POINT, Images.NE_POINT, Images.SW_POINT, Images.SE_POINT,
              Images.SEARCH, Images.MAIN_WINDOW, Images.CRAFT, Images.MY_GROUP,
              Images.ARROW, Images.AXE, Images.BACKPACK, Images.TRANSPARENCY_ON]:
        print i
        hover(i)
        assert exists(i)
    '''
    # END

    # TEST: hover trees and get trees' distances
    #     trees = main.find_trees()
    #     for tree in trees:
    #         main.hover(tree)
    #         print main.get_distance(main.get_screen_center_point(), main.get_point(tree))
    #     trees = main.get_sorted_trees(trees)
    #     for tree in trees:
    #         main.hover(tree)
    #         print main.get_distance(main.get_screen_center_point(), main.get_point(tree))
    #         sleep(1)
    # END

    # TEST: find closest tree, get to tree, come upfront
    #     main = CraftMain()
    #     tree = main.get_closest_tree()
    #     if main.go_to_tree_upfront(tree):
    #         direction = main._get_direction_to_pivot()
    #         main._pivot_to(direction)
    #     else:
    #         assert False
    # END

    # TEST: clicking around closest tree
    '''
    click_search = CraftSearch()
    tree = click_search.get_closest_tree()
    for direction in Direction.get_all_players_directions():
        click_search.click_near_tree(tree, direction)
        sleep(0.5)
    '''
    # END TEST

    # TEST: is moving
    '''
    main = CraftMain()
    main.move()
    assert not main.is_moving()
    '''
    # END TEST

    # TEST: moving aroud tree and pivot to it
    '''
    directions = Direction.get_all_players_directions()
    directions.remove(Direction.S)
    for direction in directions:
        tree = main.get_closest_tree()
        main.double_click_near_tree(tree, direction)
        main.wait_for_stop()
        direction_to_pivot = main._get_direction_to_pivot()
        main._pivot_to(direction_to_pivot)
        print main.get_player_direction(), Direction.get_opposite_direction(direction), direction
        assert main.get_player_direction() == Direction.get_opposite_direction(direction)
    #     break
    main._get_direction_to_pivot()
    '''
    # END TEST

    # TEST: moving aroud tree and is near
    '''
    main = CraftMain()
    for direction in [Direction.NE, Direction.SE, Direction.SW, Direction.NW]:
        tree = main.get_closest_tree()
        main.double_click_near_tree(tree, direction)
        main.wait_for_stop()
        tree = main.get_closest_tree()
        assert main.is_near(tree)
    '''
    # END TEST

    # TEST: hover over trees in 5 steps
#     trees = main.find_trees(False)
#     for tree in trees:
#         point = main.get_point(tree)
#         is_inside = main.is_point_inside_5_step_area(point)
#         main.hover(tree)
#         main.log("tree",tree, "point", point, "is_ inside 5 steps", is_inside)
#         sleep(1)
#
#     len1 = len(main.find_trees(False))
#     len2 = len(main.find_trees())
#     main.log(len1)
#     main.log(len2)
# END TEST

# Fighting part TODO
# ME_IN_FIGHT = Pattern("1390653549014.png").similar(0.98)
# MAGIC = "1390653583782.png"
# TACTICS = "1390653630981.png"
# TACTICS_SET = "1390653663133.png"
# INFO = False  # TODO: Add image with username
# TACTICS_INFO = "1390654068037.png"
# KICK_BLOCK = "1390654576784.png"
# BLOCK = "1390654649957.png"
# BLOCK_1 = Pattern("1390762517989.png").similar(0.90)
# BLOCK_2 = Pattern("1390762858437.png").similar(0.90)
# BLOCK_3 = Pattern("1390762881045.png").similar(0.90)
# BLOCK_4 = Pattern("1390762895399.png").similar(0.90)
# APPLY = Pattern("1390762827772.png").similar(0.90)
# click(INFO)
# wait(TACTICS)
# click(TACTICS)
# type(Key.DOWN*3+Key.TAB)
# doubleClick(TACTICS_SET)
# sleep(2)
# click(TACTICS_INFO)
# type("w", Key.CTRL)
# click(KICK_BLOCK)
# while(exists(ME_IN_FIGHT)):
#     click(KICK_BLOCK)
#     wait(BLOCK)
#     click(BLOCK_1)
#     click(BLOCK_2)
#     click(BLOCK_3)
#     click(BLOCK_4)
#     while(exists(APPLY)):
#         click(APPLY)
#     sleep(0.2)
#     waitVanish(APPLY)
#     wait(KICK_BLOCK, 3*60)
