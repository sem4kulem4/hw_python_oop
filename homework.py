from dataclasses import dataclass
from typing import Dict, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: float = 1000
    MIN_IN_H: float = 60
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_h = duration
        self.weight_kg = weight

    def duration_from_h_to_mins(self) -> float:
        return self.duration_h * self.MIN_IN_H

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.LEN_STEP * self.action / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод ещё не реализован')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration_h,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    FIRST_COEFF_CALORIE_RUN: float = 18
    SECOND_COEFF_CALORIE_RUN: float = 20

    def get_spent_calories(self) -> float:
        return ((self.FIRST_COEFF_CALORIE_RUN * self.get_mean_speed()
                - self.SECOND_COEFF_CALORIE_RUN)
                * self.weight_kg / self.M_IN_KM
                * self.duration_from_h_to_mins())


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    FIRST_COEFF_CALORIE_SWK: float = 0.035
    SECOND_COEFF_CALORIE_SWK: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height_m = height

    def get_spent_calories(self) -> float:
        return ((self.FIRST_COEFF_CALORIE_SWK * self.weight_kg
                + (self.get_mean_speed() ** 2 // self.height_m)
                * self.SECOND_COEFF_CALORIE_SWK * self.weight_kg)
                * self.duration_from_h_to_mins())


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    FIRST_COEFF_CALORIE_SWM: float = 1.1
    SECOND_COEFF_CALORIE_SWM: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.LEN_STEP * self.action / self.M_IN_KM

    def get_mean_speed(self) -> float:
        full_swimming_distance = self.length_pool * self.count_pool
        return full_swimming_distance / self.M_IN_KM / self.duration_h

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.FIRST_COEFF_CALORIE_SWM)
                * self.SECOND_COEFF_CALORIE_SWM * self.weight_kg)


def read_package(workout_type: str, data: List[int]) -> Training:
    workout_to_class: Dict[str, Type[Training]]
    workout_to_class = {'SWM': Swimming,
                        'RUN': Running,
                        'WLK': SportsWalking}
    training_class = workout_to_class.get(workout_type)
    if training_class is None:
        raise ValueError('Unknown training type')
    return training_class(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
